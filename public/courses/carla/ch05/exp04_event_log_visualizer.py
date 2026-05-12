"""实验四 趣味扩展：事件日志可视化分析器

这是一个 **纯离线** 工具，不需要 CARLA 服务器，也不依赖 matplotlib / pandas，
只用 Python 标准库。它读取上一次实验生成的 events.csv 与 summary.json，输出：

  - analysis_report.md     行为标签分布、闯红灯嫌疑表、最长红灯等待序列等文字报告
  - events_visualization.svg  四面板可视化（矢量图，浏览器直接打开）：
      Panel 1  俯视轨迹散点（按状态着色）
      Panel 2  事件时间线（每盏灯一行）
      Panel 3  行为标签条形图
      Panel 4  红灯事件速度直方图

行为标签规则（可在 BEHAVIOR_RULES 中调整）：
  - 闯红灯嫌疑 (run_red)      : light=Red, 距离 < 8 m, 速度 > 5 km/h
  - 红灯前安全停车 (stop_red) : light=Red, 速度 < 1 km/h
  - 红灯慢速接近 (slow_red)   : light=Red, 1 ≤ 速度 ≤ 15 km/h
  - 红灯远距离观察 (watch_red): light=Red, 距离 ≥ 15 m
  - 黄灯加速 (rush_yellow)    : light=Yellow, 速度 > 25 km/h
  - 黄灯减速 (yield_yellow)   : light=Yellow, 速度 ≤ 25 km/h
  - 绿灯通行 (pass_green)     : light=Green
  - 其他 (other)              : 状态为 Off / Unknown

运行示例：
  python exp04_event_log_visualizer.py
  python exp04_event_log_visualizer.py --input output/exp04 --output-dir output/exp04
"""

import argparse
import csv
import html
import json
from collections import Counter
from pathlib import Path


DEFAULT_INPUT = Path("output/exp04")


STATE_COLORS = {
    "Red": "#e53935",
    "Yellow": "#fbc02d",
    "Green": "#43a047",
    "Off": "#9e9e9e",
    "Unknown": "#9e9e9e",
}

LABEL_TEXT = {
    "run_red": "闯红灯嫌疑",
    "stop_red": "红灯前安全停车",
    "slow_red": "红灯慢速接近",
    "watch_red": "红灯远距离观察",
    "rush_yellow": "黄灯加速",
    "yield_yellow": "黄灯减速",
    "pass_green": "绿灯通行",
    "other": "其他",
}

LABEL_COLORS = {
    "run_red": "#b71c1c",
    "stop_red": "#e53935",
    "slow_red": "#ef6c00",
    "watch_red": "#f9a825",
    "rush_yellow": "#fbc02d",
    "yield_yellow": "#c0ca33",
    "pass_green": "#43a047",
    "other": "#9e9e9e",
}

LABEL_ORDER = [
    "run_red",
    "stop_red",
    "slow_red",
    "watch_red",
    "rush_yellow",
    "yield_yellow",
    "pass_green",
    "other",
]


def parse_args():
    parser = argparse.ArgumentParser(description="事件日志可视化分析器")
    parser.add_argument(
        "--input", type=Path, default=DEFAULT_INPUT,
        help="包含 events.csv 与 summary.json 的目录，默认 output/exp04",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=None,
        help="报告与可视化输出目录，默认与 --input 相同",
    )
    return parser.parse_args()


def load_events(events_path):
    if not events_path.exists():
        raise FileNotFoundError(
            f"找不到 events.csv：{events_path.resolve()}\n"
            "请先运行 carla_ch05_all_examples.py 或 exp04_traffic_light_log_answer.py 生成日志。"
        )
    with events_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = []
        for row in reader:
            row["frame"] = int(row["frame"])
            row["tick"] = int(row["tick"])
            row["sim_time_s"] = float(row["sim_time_s"])
            row["speed_kmh"] = float(row["speed_kmh"])
            row["distance_m"] = float(row["distance_m"])
            row["light_id"] = int(row["light_id"])
            row["ego_x"] = float(row["ego_x"])
            row["ego_y"] = float(row["ego_y"])
            rows.append(row)
    return rows


def load_summary(summary_path):
    if not summary_path.exists():
        return None
    return json.loads(summary_path.read_text(encoding="utf-8"))


def classify(event):
    state = event["light_state"]
    speed = event["speed_kmh"]
    distance = event["distance_m"]

    if state == "Red":
        if distance < 8.0 and speed > 5.0:
            return "run_red"
        if speed < 1.0:
            return "stop_red"
        if distance >= 15.0:
            return "watch_red"
        return "slow_red"

    if state == "Yellow":
        return "rush_yellow" if speed > 25.0 else "yield_yellow"

    if state == "Green":
        return "pass_green"

    return "other"


def ascii_bar(value, max_value, width=30):
    if max_value <= 0:
        return ""
    filled = int(round(value / max_value * width))
    return "█" * filled + "░" * (width - filled)


def find_longest_red_dwell(events):
    best = {"light_id": None, "ticks": 0, "start_tick": None, "end_tick": None}
    current_id = None
    current_start_tick = None

    for event in events:
        if event["light_state"] != "Red":
            current_id = None
            continue
        if event["light_id"] != current_id:
            current_id = event["light_id"]
            current_start_tick = event["tick"]
            continue
        span = event["tick"] - current_start_tick
        if span > best["ticks"]:
            best = {
                "light_id": current_id,
                "ticks": span,
                "start_tick": current_start_tick,
                "end_tick": event["tick"],
            }
    return best


def top_intersections(events, top_k=3):
    counter = Counter(event["light_id"] for event in events)
    return counter.most_common(top_k)


def write_markdown_report(report_path, events, summary, classified):
    label_counts = Counter(label for _, label in classified)
    total = len(events)

    lines = []
    lines.append("# 实验四 事件日志可视化分析报告\n")
    if summary:
        lines.append("## 基础参数\n")
        lines.append(f"- 运行时长（秒）: **{summary.get('run_seconds', '?')}**")
        lines.append(f"- 触发阈值（米）: **{summary.get('trigger_distance_m', '?')}**")
        lines.append(f"- 事件冷却（ticks）: **{summary.get('event_cooldown_ticks', '?')}**")
        lines.append(f"- 总事件数: **{summary.get('total_events', total)}**")
        lines.append(f"- 红灯事件: **{summary.get('red_events', '?')}**")
        lines.append(f"- 红灯占比: **{summary.get('red_ratio', '?')}**\n")

    lines.append("## 行为标签分布\n")
    max_count = max(label_counts.values()) if label_counts else 1
    lines.append("```")
    lines.append(f"{'标签':<10}{'计数':>4}  分布")
    for label in LABEL_ORDER:
        count = label_counts.get(label, 0)
        lines.append(f"{LABEL_TEXT[label]:<10}{count:>4}  {ascii_bar(count, max_count)}")
    lines.append("```\n")

    suspects = [event for event, label in classified if label == "run_red"]
    lines.append("## 闯红灯嫌疑事件（红灯 + 距离<8m + 速度>5km/h）\n")
    if suspects:
        lines.append("| frame | sim_time_s | 速度(km/h) | 距离(m) | light_id | 位置(x, y) |")
        lines.append("| ----- | ---------- | ---------- | ------- | -------- | ---------- |")
        for event in suspects[:10]:
            lines.append(
                f"| {event['frame']} | {event['sim_time_s']:.2f} | "
                f"{event['speed_kmh']:.2f} | {event['distance_m']:.2f} | "
                f"{event['light_id']} | ({event['ego_x']:.1f}, {event['ego_y']:.1f}) |"
            )
        if len(suspects) > 10:
            lines.append(f"\n（共 {len(suspects)} 条，仅展示前 10 条）")
        lines.append("")
    else:
        lines.append("没有发现闯红灯嫌疑事件，自动驾驶在红灯前都减速或停车了。\n")

    lines.append("## 最长红灯等待序列\n")
    longest = find_longest_red_dwell(events)
    if longest["light_id"] is not None and longest["ticks"] > 0:
        seconds = longest["ticks"] * 0.05
        lines.append(
            f"- 交通灯 **{longest['light_id']}** 上连续命中红灯事件，从 tick {longest['start_tick']} "
            f"到 tick {longest['end_tick']}，跨度约 **{seconds:.1f} s**。\n"
        )
    else:
        lines.append("没有出现连续的红灯等待序列。\n")

    lines.append("## 最常遇到的交通灯 Top 3\n")
    top = top_intersections(events, top_k=3)
    if top:
        lines.append("| 排名 | light_id | 事件次数 |")
        lines.append("| ---- | -------- | -------- |")
        for index, (light_id, count) in enumerate(top, start=1):
            lines.append(f"| {index} | {light_id} | {count} |")
        lines.append("")

    lines.append("## 配套可视化\n")
    lines.append(
        "本报告附带 `events_visualization.svg`：四面板矢量图，可在浏览器中直接打开。"
        "面板 1 为俯视轨迹散点（按状态着色），面板 2 为事件时间线，"
        "面板 3 为行为标签条形图，面板 4 为红灯事件速度直方图。\n"
    )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------- #
# SVG 生成
# --------------------------------------------------------------------------- #

SVG_WIDTH = 1080
SVG_HEIGHT = 760
PANEL_GAP = 24
TOP_OFFSET = 70

PANEL_W = (SVG_WIDTH - PANEL_GAP * 3) / 2
PANEL_H = (SVG_HEIGHT - TOP_OFFSET - PANEL_GAP * 3) / 2


def svg_text(x, y, text, size=12, color="#222", anchor="start", weight="normal"):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" '
        f'font-family="Segoe UI, Helvetica, sans-serif" '
        f'font-size="{size}" fill="{color}" text-anchor="{anchor}" '
        f'font-weight="{weight}">{html.escape(str(text))}</text>'
    )


def svg_rect(x, y, w, h, fill="#fff", stroke="#e0e0e0"):
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'fill="{fill}" stroke="{stroke}" rx="6" ry="6"/>'
    )


def panel_frame(x, y, title, subtitle=None):
    parts = [
        svg_rect(x, y, PANEL_W, PANEL_H, fill="#fafafa", stroke="#d6d8db"),
        svg_text(x + 12, y + 24, title, size=15, color="#222", weight="bold"),
    ]
    if subtitle:
        parts.append(svg_text(x + 12, y + 42, subtitle, size=11, color="#666"))
    return "\n".join(parts)


def panel_trajectory(x, y, events):
    out = [panel_frame(x, y, "俯视轨迹散点", "圆点颜色 = 交通灯状态；箭头 = 行驶方向")]

    if not events:
        out.append(svg_text(x + PANEL_W / 2, y + PANEL_H / 2, "无事件数据", anchor="middle", color="#999"))
        return "\n".join(out)

    xs = [event["ego_x"] for event in events]
    ys = [event["ego_y"] for event in events]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    span_x = max(x_max - x_min, 1e-6)
    span_y = max(y_max - y_min, 1e-6)
    span = max(span_x, span_y) * 1.1

    plot_x = x + 50
    plot_y = y + 60
    plot_w = PANEL_W - 70
    plot_h = PANEL_H - 90

    cx = (x_min + x_max) / 2
    cy = (y_min + y_max) / 2

    def to_screen(px, py):
        sx = plot_x + plot_w / 2 + (px - cx) / span * plot_w
        sy = plot_y + plot_h / 2 - (py - cy) / span * plot_h
        return sx, sy

    out.append(svg_rect(plot_x, plot_y, plot_w, plot_h, fill="#ffffff", stroke="#eee"))

    pts = [to_screen(event["ego_x"], event["ego_y"]) for event in events]
    if len(pts) >= 2:
        path = "M" + " L".join(f"{sx:.1f},{sy:.1f}" for sx, sy in pts)
        out.append(f'<path d="{path}" fill="none" stroke="#bbb" stroke-width="1" stroke-dasharray="3 2"/>')

    for event, (sx, sy) in zip(events, pts):
        color = STATE_COLORS.get(event["light_state"], "#777")
        out.append(
            f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="5" '
            f'fill="{color}" fill-opacity="0.85" stroke="white" stroke-width="1"/>'
        )

    if len(pts) >= 2:
        first_x, first_y = pts[0]
        last_x, last_y = pts[-1]
        out.append(
            f'<circle cx="{first_x:.1f}" cy="{first_y:.1f}" r="9" fill="none" '
            f'stroke="#1976d2" stroke-width="2"/>'
        )
        out.append(svg_text(first_x + 10, first_y - 8, "起点", size=10, color="#1976d2"))
        out.append(
            f'<circle cx="{last_x:.1f}" cy="{last_y:.1f}" r="9" fill="none" '
            f'stroke="#6a1b9a" stroke-width="2"/>'
        )
        out.append(svg_text(last_x + 10, last_y + 12, "终点", size=10, color="#6a1b9a"))

    legend_x = plot_x
    legend_y = plot_y + plot_h + 16
    for index, state in enumerate(["Red", "Yellow", "Green"]):
        cx_l = legend_x + index * 90
        out.append(
            f'<circle cx="{cx_l + 6:.1f}" cy="{legend_y:.1f}" r="5" '
            f'fill="{STATE_COLORS[state]}"/>'
        )
        out.append(svg_text(cx_l + 16, legend_y + 4, state, size=11, color="#444"))

    out.append(svg_text(plot_x, plot_y - 6, f"x: {x_min:.1f} … {x_max:.1f} m", size=10, color="#888"))
    out.append(svg_text(plot_x + plot_w, plot_y - 6, f"y: {y_min:.1f} … {y_max:.1f} m",
                        size=10, color="#888", anchor="end"))
    return "\n".join(out)


def panel_timeline(x, y, events):
    out = [panel_frame(x, y, "事件时间线", "x 轴 = 仿真时间秒；y 轴 = 交通灯 id")]

    if not events:
        out.append(svg_text(x + PANEL_W / 2, y + PANEL_H / 2, "无事件数据", anchor="middle", color="#999"))
        return "\n".join(out)

    plot_x = x + 50
    plot_y = y + 60
    plot_w = PANEL_W - 70
    plot_h = PANEL_H - 90

    out.append(svg_rect(plot_x, plot_y, plot_w, plot_h, fill="#ffffff", stroke="#eee"))

    times = [event["sim_time_s"] for event in events]
    t_min, t_max = min(times), max(times)
    span_t = max(t_max - t_min, 1e-6)

    light_ids = sorted({event["light_id"] for event in events})
    if not light_ids:
        return "\n".join(out)
    id_index = {lid: idx for idx, lid in enumerate(light_ids)}
    rows = len(light_ids)
    row_h = plot_h / max(rows, 1)

    for idx, lid in enumerate(light_ids):
        cy = plot_y + idx * row_h + row_h / 2
        out.append(
            f'<line x1="{plot_x:.1f}" y1="{cy:.1f}" '
            f'x2="{plot_x + plot_w:.1f}" y2="{cy:.1f}" '
            f'stroke="#f1f1f1" stroke-width="1"/>'
        )
        out.append(svg_text(plot_x - 6, cy + 4, f"#{lid}", size=10, color="#666", anchor="end"))

    for event in events:
        ratio = (event["sim_time_s"] - t_min) / span_t
        sx = plot_x + ratio * plot_w
        sy = plot_y + id_index[event["light_id"]] * row_h + row_h / 2
        color = STATE_COLORS.get(event["light_state"], "#777")
        out.append(
            f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="5" '
            f'fill="{color}" fill-opacity="0.85" stroke="white" stroke-width="1"/>'
        )

    out.append(svg_text(plot_x, plot_y + plot_h + 16, f"{t_min:.1f} s", size=10, color="#666"))
    out.append(svg_text(plot_x + plot_w, plot_y + plot_h + 16,
                        f"{t_max:.1f} s", size=10, color="#666", anchor="end"))
    return "\n".join(out)


def panel_label_bars(x, y, classified):
    out = [panel_frame(x, y, "行为标签条形图", "按规则给每条事件打标签后汇总")]

    label_counts = Counter(label for _, label in classified)
    max_count = max(label_counts.values()) if label_counts else 1

    plot_x = x + 130
    plot_y = y + 60
    plot_w = PANEL_W - 160
    plot_h = PANEL_H - 90

    row_h = plot_h / len(LABEL_ORDER)
    for idx, label in enumerate(LABEL_ORDER):
        count = label_counts.get(label, 0)
        cy = plot_y + idx * row_h + row_h / 2
        bar_w = (count / max_count) * plot_w if max_count else 0
        out.append(svg_text(plot_x - 8, cy + 4, LABEL_TEXT[label], size=11, color="#444", anchor="end"))
        out.append(
            f'<rect x="{plot_x:.1f}" y="{cy - row_h / 2 + 6:.1f}" '
            f'width="{bar_w:.1f}" height="{max(row_h - 12, 4):.1f}" '
            f'fill="{LABEL_COLORS[label]}" rx="3" ry="3"/>'
        )
        out.append(svg_text(plot_x + bar_w + 6, cy + 4, str(count), size=11, color="#222"))
    return "\n".join(out)


def panel_red_speed_hist(x, y, events):
    out = [panel_frame(x, y, "红灯事件速度直方图", "x = km/h，y = 红灯事件数")]

    red_events = [event for event in events if event["light_state"] == "Red"]
    plot_x = x + 50
    plot_y = y + 60
    plot_w = PANEL_W - 70
    plot_h = PANEL_H - 90

    out.append(svg_rect(plot_x, plot_y, plot_w, plot_h, fill="#ffffff", stroke="#eee"))

    if not red_events:
        out.append(svg_text(x + PANEL_W / 2, y + PANEL_H / 2, "无红灯事件",
                            anchor="middle", color="#999"))
        return "\n".join(out)

    speeds = [event["speed_kmh"] for event in red_events]
    bins = [(0, 1), (1, 5), (5, 10), (10, 20), (20, 40), (40, 200)]
    bin_labels = ["<1", "1-5", "5-10", "10-20", "20-40", "≥40"]
    bin_counts = [sum(1 for s in speeds if low <= s < high) for low, high in bins]
    max_count = max(bin_counts) if max(bin_counts) > 0 else 1

    bar_w = plot_w / len(bins)
    for idx, (count, label) in enumerate(zip(bin_counts, bin_labels)):
        bar_h = (count / max_count) * (plot_h - 30)
        bx = plot_x + idx * bar_w + bar_w * 0.15
        by = plot_y + plot_h - 20 - bar_h
        out.append(
            f'<rect x="{bx:.1f}" y="{by:.1f}" '
            f'width="{bar_w * 0.7:.1f}" height="{bar_h:.1f}" '
            f'fill="#e53935" fill-opacity="0.85" rx="3" ry="3"/>'
        )
        if count:
            out.append(svg_text(bx + bar_w * 0.35, by - 4, str(count),
                                size=10, color="#b71c1c", anchor="middle"))
        out.append(svg_text(bx + bar_w * 0.35, plot_y + plot_h - 4, label,
                            size=10, color="#666", anchor="middle"))

    avg = sum(speeds) / len(speeds)
    out.append(svg_text(plot_x, plot_y + 18, f"平均: {avg:.2f} km/h", size=11, color="#444"))
    return "\n".join(out)


def render_svg(svg_path, events, summary, classified):
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" '
        f'viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">',
        svg_rect(0, 0, SVG_WIDTH, SVG_HEIGHT, fill="#f4f5f7", stroke="none"),
        svg_text(SVG_WIDTH / 2, 36, "实验四 事件日志可视化分析", size=22, color="#111",
                 anchor="middle", weight="bold"),
    ]
    summary_line = ""
    if summary:
        summary_line = (
            f"运行 {summary.get('run_seconds', '?')} s  ·  "
            f"阈值 {summary.get('trigger_distance_m', '?')} m  ·  "
            f"总事件 {summary.get('total_events', len(events))}  ·  "
            f"红灯 {summary.get('red_events', '?')}  ·  "
            f"红灯占比 {summary.get('red_ratio', '?')}"
        )
    else:
        summary_line = f"共 {len(events)} 条事件"
    parts.append(svg_text(SVG_WIDTH / 2, 58, summary_line, size=12, color="#555", anchor="middle"))

    x_left = PANEL_GAP
    x_right = PANEL_GAP + PANEL_W + PANEL_GAP
    y_top = TOP_OFFSET
    y_bottom = TOP_OFFSET + PANEL_H + PANEL_GAP

    parts.append(panel_trajectory(x_left, y_top, events))
    parts.append(panel_timeline(x_right, y_top, events))
    parts.append(panel_label_bars(x_left, y_bottom, classified))
    parts.append(panel_red_speed_hist(x_right, y_bottom, events))

    parts.append("</svg>")
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text("\n".join(parts), encoding="utf-8")


def main():
    args = parse_args()
    events_path = args.input / "events.csv"
    summary_path = args.input / "summary.json"
    out_dir = args.output_dir if args.output_dir is not None else args.input

    events = load_events(events_path)
    summary = load_summary(summary_path)
    classified = [(event, classify(event)) for event in events]

    report_path = out_dir / "analysis_report.md"
    svg_path = out_dir / "events_visualization.svg"
    write_markdown_report(report_path, events, summary, classified)
    render_svg(svg_path, events, summary, classified)

    print(f"读取事件：{len(events)} 条  来源：{events_path.resolve()}")
    print(f"Markdown 报告：{report_path.resolve()}")
    print(f"SVG 可视化：  {svg_path.resolve()}")
    print("\n用浏览器打开 SVG 文件即可看到四面板可视化。")


if __name__ == "__main__":
    main()
