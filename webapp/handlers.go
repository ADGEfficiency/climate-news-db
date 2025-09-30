package main

import (
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

func (h *Handlers) Dashboard(c *gin.Context) {
	stats, err := h.db.GetNewspaperStats()
	if err != nil {
		c.HTML(http.StatusInternalServerError, "error.html", gin.H{
			"error": err.Error(),
		})
		return
	}

	c.HTML(http.StatusOK, "dashboard.html", gin.H{
		"title":      "Climate News Dashboard",
		"newspapers": stats,
	})
}

func (h *Handlers) Article(c *gin.Context) {
	idStr := c.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		c.HTML(http.StatusBadRequest, "error.html", gin.H{
			"error": "Invalid article ID",
		})
		return
	}

	article, err := h.db.GetArticleByID(id)
	if err != nil {
		c.HTML(http.StatusNotFound, "error.html", gin.H{
			"error": "Article not found",
		})
		return
	}

	c.HTML(http.StatusOK, "article.html", gin.H{
		"title":   "Article - " + article.Headline,
		"article": article,
	})
}

func (h *Handlers) Latest(c *gin.Context) {
	latestPublished, err := h.db.GetLatestPublishedArticles(50)
	if err != nil {
		c.HTML(http.StatusInternalServerError, "error.html", gin.H{
			"error": err.Error(),
		})
		return
	}

	c.HTML(http.StatusOK, "latest.html", gin.H{
		"title":           "Latest Articles",
		"latestPublished": latestPublished,
	})
}