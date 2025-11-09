package main

import (
	"database/sql"
	"math/rand"
)

type NewspaperStats struct {
	Name                 string  `json:"name"`
	FancyName            string  `json:"fancy_name"`
	Site                 string  `json:"site"`
	Color                string  `json:"color"`
	ArticleCount         int     `json:"article_count"`
	AverageArticleLength float64 `json:"average_article_length"`
}

type Article struct {
	ID              int    `json:"id"`
	ArticleName     string `json:"article_name"`
	Headline        string `json:"headline"`
	Body            string `json:"body"`
	DatePublished   string `json:"date_published"`
	ArticleURL      string `json:"article_url"`
	DatetimeCrawled string `json:"datetime_crawled_utc"`
	ArticleLength   int    `json:"article_length"`
	NewspaperID     int    `json:"newspaper_id"`
	NewspaperName   string `json:"newspaper_name"`
	NewspaperFancy  string `json:"newspaper_fancy"`
	NewspaperSite   string `json:"newspaper_site"`
	NewspaperColor  string `json:"newspaper_color"`
}

type Database struct {
	db *sql.DB
}

func NewDatabase(dbPath string) (*Database, error) {
	db, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		return nil, err
	}

	if err := db.Ping(); err != nil {
		return nil, err
	}

	return &Database{db: db}, nil
}

func (d *Database) GetNewspaperStats() ([]NewspaperStats, error) {
	query := `
		SELECT
			n.name,
			n.fancy_name,
			n.site,
			n.color,
			COUNT(a.id) as article_count,
			COALESCE(AVG(a.article_length), 0) as average_article_length
		FROM newspaper n
		LEFT JOIN article a ON n.id = a.newspaper_id
		GROUP BY n.id, n.name, n.fancy_name, n.site, n.color
		ORDER BY n.name ASC
	`

	rows, err := d.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var stats []NewspaperStats
	for rows.Next() {
		var stat NewspaperStats
		err := rows.Scan(&stat.Name, &stat.FancyName, &stat.Site, &stat.Color, &stat.ArticleCount, &stat.AverageArticleLength)
		if err != nil {
			return nil, err
		}
		stats = append(stats, stat)
	}

	return stats, nil
}

func (d *Database) GetArticleByID(id int) (*Article, error) {
	query := `
		SELECT
			a.id, a.article_name, a.headline, a.body, a.date_published,
			a.article_url, a.datetime_crawled_utc, a.article_length,
			a.newspaper_id, n.name, n.fancy_name, n.site, n.color
		FROM article a
		JOIN newspaper n ON a.newspaper_id = n.id
		WHERE a.id = ?
	`

	var article Article
	err := d.db.QueryRow(query, id).Scan(
		&article.ID, &article.ArticleName, &article.Headline, &article.Body,
		&article.DatePublished, &article.ArticleURL, &article.DatetimeCrawled,
		&article.ArticleLength, &article.NewspaperID, &article.NewspaperName,
		&article.NewspaperFancy, &article.NewspaperSite, &article.NewspaperColor,
	)

	if err != nil {
		return nil, err
	}

	return &article, nil
}

func (d *Database) GetLatestPublishedArticles(limit int) ([]Article, error) {
	query := `
		SELECT
			a.id, a.article_name, a.headline, a.body, a.date_published,
			a.article_url, a.datetime_crawled_utc, a.article_length,
			a.newspaper_id, n.name, n.fancy_name, n.site, n.color
		FROM article a
		JOIN newspaper n ON a.newspaper_id = n.id
		ORDER BY a.date_published DESC
		LIMIT ?
	`

	rows, err := d.db.Query(query, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var articles []Article
	for rows.Next() {
		var article Article
		err := rows.Scan(
			&article.ID, &article.ArticleName, &article.Headline, &article.Body,
			&article.DatePublished, &article.ArticleURL, &article.DatetimeCrawled,
			&article.ArticleLength, &article.NewspaperID, &article.NewspaperName,
			&article.NewspaperFancy, &article.NewspaperSite, &article.NewspaperColor,
		)
		if err != nil {
			return nil, err
		}
		articles = append(articles, article)
	}

	return articles, nil
}

func (d *Database) GetLatestScrapedArticles(limit int) ([]Article, error) {
	query := `
		SELECT
			a.id, a.article_name, a.headline, a.body, a.date_published,
			a.article_url, a.datetime_crawled_utc, a.article_length,
			a.newspaper_id, n.name, n.fancy_name, n.site, n.color
		FROM article a
		JOIN newspaper n ON a.newspaper_id = n.id
		ORDER BY a.datetime_crawled_utc DESC
		LIMIT ?
	`

	rows, err := d.db.Query(query, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var articles []Article
	for rows.Next() {
		var article Article
		err := rows.Scan(
			&article.ID, &article.ArticleName, &article.Headline, &article.Body,
			&article.DatePublished, &article.ArticleURL, &article.DatetimeCrawled,
			&article.ArticleLength, &article.NewspaperID, &article.NewspaperName,
			&article.NewspaperFancy, &article.NewspaperSite, &article.NewspaperColor,
		)
		if err != nil {
			return nil, err
		}
		articles = append(articles, article)
	}

	return articles, nil
}

func (d *Database) GetRandomArticleID() (int, error) {
	query := `SELECT MIN(id), MAX(id) FROM article`

	var minID, maxID int
	err := d.db.QueryRow(query).Scan(&minID, &maxID)
	if err != nil {
		return 0, err
	}

	return rand.Intn(maxID-minID+1) + minID, nil
}

func (d *Database) GetArticlesByNewspaper(newspaperName string) ([]Article, error) {
	query := `
		SELECT
			a.id, a.article_name, a.headline, a.body, a.date_published,
			a.article_url, a.datetime_crawled_utc, a.article_length,
			a.newspaper_id, n.name, n.fancy_name, n.site, n.color
		FROM article a
		JOIN newspaper n ON a.newspaper_id = n.id
		WHERE n.name = ?
		ORDER BY a.date_published DESC
	`

	rows, err := d.db.Query(query, newspaperName)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var articles []Article
	for rows.Next() {
		var article Article
		err := rows.Scan(
			&article.ID, &article.ArticleName, &article.Headline, &article.Body,
			&article.DatePublished, &article.ArticleURL, &article.DatetimeCrawled,
			&article.ArticleLength, &article.NewspaperID, &article.NewspaperName,
			&article.NewspaperFancy, &article.NewspaperSite, &article.NewspaperColor,
		)
		if err != nil {
			return nil, err
		}
		articles = append(articles, article)
	}

	return articles, nil
}

func (d *Database) Close() error {
	return d.db.Close()
}
