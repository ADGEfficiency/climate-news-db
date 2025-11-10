package main

import (
	"fmt"
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
		"timeAgo": func(dateStr string) string {
			if dateStr == "" {
				return "-"
			}

			// Remove UTC suffix if present
			dateStr = strings.TrimSuffix(strings.TrimSpace(dateStr), "UTC")

			// Parse format: 2021-01-01T01:16:17.000000
			t, err := time.Parse("2006-01-02T15:04:05.999999", dateStr)
			if err != nil {
				return "unknown"
			}

			duration := time.Since(t)
			days := int(duration.Hours() / 24)

			if days > 365 {
				years := days / 365
				if years == 1 {
					return "1 year"
				}
				return fmt.Sprintf("%d years", years)
			} else if days > 30 {
				months := days / 30
				if months == 1 {
					return "1 month"
				}
				return fmt.Sprintf("%d months", months)
			} else if days > 0 {
				if days == 1 {
					return "1 day"
				}
				return fmt.Sprintf("%d days", days)
			}
			return "0 days"
		},
		"extractDate": func(dateStr string) string {
			if dateStr == "" {
				return "-"
			}

			// Simply extract the date part (YYYY-MM-DD) from the beginning
			if len(dateStr) >= 10 {
				return dateStr[:10]
			}
			return dateStr
		},
		"freshnessClass": func(dateStr string) string {
			if dateStr == "" {
				return "text-gray-500"
			}

			// Remove UTC suffix if present
			dateStr = strings.TrimSuffix(strings.TrimSpace(dateStr), "UTC")

			// Parse format: 2021-01-01T01:16:17.000000
			t, err := time.Parse("2006-01-02T15:04:05.999999", dateStr)
			if err != nil {
				return "text-gray-500"
			}

			duration := time.Since(t)
			days := int(duration.Hours() / 24)

			// Green: < 1 day (fresh)
			if days < 1 {
				return "text-green-600"
			}
			// Yellow/Orange: 1-7 days (stale)
			if days < 7 {
				return "text-yellow-600"
			}
			// Red: > 7 days (very old)
			return "text-red-600"
		},
	}

	// Load templates with custom functions
	r.SetFuncMap(funcMap)
	r.LoadHTMLGlob("src/webapp/templates/*")

	// Serve static files
	r.Static("/static", "static")

	// Routes
	r.GET("/", handlers.Newspapers)
	r.GET("/latest", handlers.Latest)
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
