package main

import (
	"fmt"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

type Handlers struct {
	db *Database
}

func NewHandlers(db *Database) *Handlers {
	return &Handlers{db: db}
}

func (h *Handlers) Newspapers(c *gin.Context) {
	stats, err := h.db.GetNewspaperStats()
	if err != nil {
		c.HTML(http.StatusInternalServerError, "error.html", gin.H{
			"title": AppTitle,
			"error": err.Error(),
		})
		return
	}

	c.HTML(http.StatusOK, "dashboard.html", gin.H{
		"title":      AppTitle,
		"newspapers": stats,
	})
}

func (h *Handlers) Article(c *gin.Context) {
	idStr := c.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		c.HTML(http.StatusBadRequest, "error.html", gin.H{
			"title": AppTitle,
			"error": "Invalid article ID",
		})
		return
	}

	article, err := h.db.GetArticleByID(id)
	if err != nil {
		c.HTML(http.StatusNotFound, "error.html", gin.H{
			"title": AppTitle,
			"error": "Article not found",
		})
		return
	}

	c.HTML(http.StatusOK, "article.html", gin.H{
		"title":   AppTitle,
		"article": article,
	})
}

func (h *Handlers) Latest(c *gin.Context) {
	latestPublished, err := h.db.GetLatestPublishedArticles(20)
	if err != nil {
		c.HTML(http.StatusInternalServerError, "error.html", gin.H{
			"title": AppTitle,
			"error": err.Error(),
		})
		return
	}

	c.HTML(http.StatusOK, "latest.html", gin.H{
		"title":           AppTitle,
		"latestPublished": latestPublished,
	})
}

func (h *Handlers) Random(c *gin.Context) {
	id, err := h.db.GetRandomArticleID()
	if err != nil {
		c.HTML(http.StatusInternalServerError, "error.html", gin.H{
			"title": AppTitle,
			"error": err.Error(),
		})
		return
	}

	c.Redirect(http.StatusFound, fmt.Sprintf("/article/%d", id))
}

func (h *Handlers) Newspaper(c *gin.Context) {
	newspaperName := c.Param("newspaper")

	articles, err := h.db.GetArticlesByNewspaper(newspaperName)
	if err != nil {
		c.HTML(http.StatusInternalServerError, "error.html", gin.H{
			"title": AppTitle,
			"error": err.Error(),
		})
		return
	}

	if len(articles) == 0 {
		c.HTML(http.StatusNotFound, "error.html", gin.H{
			"title": AppTitle,
			"error": "Newspaper not found",
		})
		return
	}

	// Get newspaper info from first article
	newspaper := articles[0]

	// Get latest article date (articles are sorted by date_published DESC)
	latestArticleDate := ""
	if len(articles) > 0 {
		latestArticleDate = articles[0].DatePublished
	}

	c.HTML(http.StatusOK, "newspaper.html", gin.H{
		"title":             AppTitle,
		"newspaperName":     newspaper.NewspaperName,
		"newspaperFancy":    newspaper.NewspaperFancy,
		"newspaperSite":     newspaper.NewspaperSite,
		"newspaperColor":    newspaper.NewspaperColor,
		"articles":          articles,
		"articleCount":      len(articles),
		"latestArticleDate": latestArticleDate,
	})
}

func (h *Handlers) Download(c *gin.Context) {
	zipPath := "data/climate-news-db-dataset.zip"
	c.FileAttachment(zipPath, "climate-news-db-dataset.zip")
}
