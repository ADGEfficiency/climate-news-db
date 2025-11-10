package main

import (
	"html/template"
	"log"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	_ "github.com/mattn/go-sqlite3"
)

const AppTitle = "climate-news-db"

func main() {
	// Initialize database
	dbPath := "data/db.sqlite"
	db, err := NewDatabase(dbPath)
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
	defer db.Close()

	// Initialize handlers
	handlers := NewHandlers(db)

	// Setup Gin router
	r := gin.Default()

	// Custom template functions
	funcMap := template.FuncMap{
		"add":     func(a, b int) int { return a + b },
		"div":     func(a, b float64) float64 { return a / b },
		"float64": func(i int) float64 { return float64(i) },
		"formatDate": func(dateStr string) string {
			// Handle empty strings
			if dateStr == "" {
				return "-"
			}

			// Try parsing various timestamp formats
			formats := []string{
				time.RFC3339,
				"2006-01-02 15:04:05",
				"2006-01-02T15:04:05",
				"2006-01-02",
			}

			var t time.Time
			var err error

			for _, format := range formats {
				t, err = time.Parse(format, strings.TrimSpace(dateStr))
				if err == nil {
					break
				}
			}

			// If parsing failed, return original string
			if err != nil {
				return dateStr
			}

			// Format as readable date
			return t.Format("Jan 2, 2006")
		},
		"formatDateTime": func(dateStr string) string {
			// Handle empty strings
			if dateStr == "" {
				return "-"
			}

			// Try parsing various timestamp formats
			formats := []string{
				time.RFC3339,
				"2006-01-02 15:04:05",
				"2006-01-02T15:04:05",
				"2006-01-02",
			}

			var t time.Time
			var err error

			for _, format := range formats {
				t, err = time.Parse(format, strings.TrimSpace(dateStr))
				if err == nil {
					break
				}
			}

			// If parsing failed, return original string
			if err != nil {
				return dateStr
			}

			// Format as readable date and time
			return t.Format("Jan 2, 2006 at 3:04 PM")
		},
	}

	// Load templates with custom functions
	r.SetFuncMap(funcMap)
	r.LoadHTMLGlob("src/webapp/templates/*")

	// Serve static files
	r.Static("/static", "static")

	// Routes
	r.GET("/", handlers.Latest)
	r.GET("/newspapers", handlers.Dashboard)
	r.GET("/newspaper/:newspaper", handlers.Newspaper)
	r.GET("/article/:id", handlers.Article)
	r.GET("/random", handlers.Random)
	r.GET("/download", handlers.Download)

	// Start server
	log.Println("Starting server on :8080")
	log.Println("Visit http://localhost:8080 to view the dashboard")
	if err := r.Run(":8080"); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
