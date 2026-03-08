CREATE TABLE IF NOT EXISTS `page_views` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `path` VARCHAR(255) NOT NULL,
  `chapter_id` VARCHAR(64) NULL,
  `session_id` VARCHAR(128) NOT NULL,
  `referrer` VARCHAR(500) NULL,
  `user_agent` VARCHAR(500) NULL,
  `ip_address` VARCHAR(64) NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_page_views_path` (`path`),
  KEY `idx_page_views_chapter_id` (`chapter_id`),
  KEY `idx_page_views_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
