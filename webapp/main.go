package main

import (
	"html/template"
	"log"

	"github.com/gin-gonic/gin"
	_ "github.com/mattn/go-sqlite3"
)

func main() {
	// Initialize database
	dbPath := "../data/db.sqlite"
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
	}

	// Load templates with custom functions
	r.SetFuncMap(funcMap)
	r.LoadHTMLGlob("templates/*")

	// Routes
	r.GET("/", handlers.Latest)
	r.GET("/newspapers", handlers.Dashboard)
	r.GET("/article/:id", handlers.Article)
	r.GET("/random", handlers.Random)

	// Start server
	log.Println("Starting server on :8080")
	log.Println("Visit http://localhost:8080 to view the dashboard")
	if err := r.Run(":8080"); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}