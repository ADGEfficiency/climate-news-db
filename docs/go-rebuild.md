# Go Webapp Rebuild Documentation

## Overview

This document describes the Go webapp rebuild that provides a modern, responsive dashboard for visualizing climate news data from the SQLite database.

## Go Climate News Dashboard

### Architecture

The Go webapp is built using:
- **Gin** - Fast HTTP web framework for Go
- **SQLite3** - Database driver for accessing the existing database
- **Tailwind CSS** - Utility-first CSS framework for styling
- **HTMX** - For dynamic content loading without full page reloads
- **Chart.js** - For interactive data visualizations

### Project Structure

```
webapp/
├── go.mod                 # Go module dependencies
├── main.go               # Main server setup and routes
├── models.go             # Database models and query functions
├── handlers.go           # HTTP request handlers
├── templates/
│   ├── dashboard.html    # Main dashboard template
│   ├── chart.html        # Chart component template
│   └── error.html        # Error page template
├── test-webapp.js        # Playwright test script
├── package.json          # Node.js dependencies for testing
└── webapp-screenshot.png # Test screenshot output
```

### Key Features

#### 1. Dashboard Overview
- **Statistics Cards**: Display total newspapers (22), total articles (16,532), and average article length
- **Responsive Design**: Mobile-friendly layout using Tailwind CSS grid system
- **Clean UI**: Professional dashboard interface with proper spacing and typography

#### 2. Interactive Chart
- **Yearly Aggregation**: Articles grouped by year instead of individual dates for better readability
- **Multi-newspaper Support**: Different colored lines for each newspaper source
- **Dynamic Loading**: Chart loads via HTMX for smooth user experience
- **Chart.js Integration**: Interactive tooltips, legends, and responsive design

#### 3. Newspaper Table
- **Complete Overview**: Lists all 22 newspapers with their statistics
- **Color Coding**: Each newspaper has a unique color indicator
- **Article Counts**: Real-time article counts calculated from database
- **External Links**: Direct links to newspaper websites
- **Sortable Data**: Newspapers ordered by article count (descending)

### Database Integration

#### Models (`models.go`)

```go
type NewspaperStats struct {
    Name                  string  `json:"name"`
    FancyName             string  `json:"fancy_name"`
    Site                  string  `json:"site"`
    Color                 string  `json:"color"`
    ArticleCount          int     `json:"article_count"`
    AverageArticleLength  float64 `json:"average_article_length"`
}

type TimeSeriesData struct {
    Date         string `json:"date"`
    NewspaperName string `json:"newspaper_name"`
    Count        int    `json:"count"`
}
```

#### Key Queries

**Newspaper Statistics:**
```sql
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
ORDER BY article_count DESC
```

**Time Series Data (Yearly):**
```sql
SELECT
    strftime('%Y', a.date_published) as date,
    n.fancy_name as newspaper_name,
    COUNT(*) as count
FROM article a
JOIN newspaper n ON a.newspaper_id = n.id
GROUP BY strftime('%Y', a.date_published), n.fancy_name
ORDER BY date DESC, newspaper_name
```

### API Endpoints

- `GET /` - Main dashboard page
- `GET /chart` - Chart component (loaded via HTMX)
- `GET /api/timeseries` - JSON API for chart data

### Frontend Technologies

#### Tailwind CSS Classes Used
- `bg-gray-50` - Light gray background
- `max-w-7xl mx-auto` - Responsive container with centered layout
- `grid grid-cols-1 md:grid-cols-3` - Responsive grid for statistics cards
- `shadow rounded-lg` - Card styling with shadows and rounded corners
- `hover:bg-gray-50` - Interactive hover states

#### HTMX Integration
```html
<div id="chart-container"
     hx-get="/chart"
     hx-trigger="load"
     class="h-96">
    <div class="flex items-center justify-center h-full">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
</div>
```

#### Chart.js Configuration
- **Type**: Line chart for time series data
- **Responsive**: Maintains aspect ratio across devices
- **Scales**: Proper labeling for X (Year) and Y (Article Count) axes
- **Plugins**: Title, legend with point styles, and hover interactions

### Development and Testing

#### Running the Application

1. **Install Dependencies:**
   ```bash
   cd webapp
   go mod tidy
   ```

2. **Start the Server:**
   ```bash
   go run .
   ```
   Server starts on `http://localhost:8080`

#### Testing with Playwright

The webapp includes automated testing using Playwright:

```bash
# Install Playwright and dependencies
npm install playwright
npx playwright install

# Run tests (ensure server is running first)
node test-webapp.js
```

**Test Coverage:**
- Server connectivity verification
- Page title validation
- Statistics cards presence (3 cards)
- Chart container visibility
- Newspaper table presence (22 rows)
- Chart loading via HTMX
- Screenshot capture for visual verification

### Template System

#### Go Template Features Used
- **Custom Functions**: `add`, `div`, `float64` for calculations
- **Range Iterations**: Loop through newspapers and statistics
- **Conditional Logic**: Display logic for data presentation
- **HTML Escaping**: Automatic escaping for security

#### Template Structure
```go
// Custom template functions
funcMap := template.FuncMap{
    "add":     func(a, b int) int { return a + b },
    "div":     func(a, b float64) float64 { return a / b },
    "float64": func(i int) float64 { return float64(i) },
}

// Load templates
r.SetFuncMap(funcMap)
r.LoadHTMLGlob("templates/*")
```

### Performance Optimizations

1. **Database Connection Pooling**: Single connection reused across requests
2. **Efficient Queries**: Aggregated data queries to minimize database calls
3. **Static Asset CDN**: External CDN for Tailwind, HTMX, and Chart.js
4. **Responsive Images**: No heavy images, relies on CSS and SVG icons
5. **HTMX Lazy Loading**: Chart loads only when page is ready

### Error Handling

- **Database Errors**: Graceful fallback with error page template
- **Template Errors**: Server-side validation with fallback values
- **404 Handling**: Gin's built-in 404 handling
- **HTMX Timeouts**: Loading spinners with timeout handling

### Security Considerations

- **SQL Injection Prevention**: Parameterized queries throughout
- **XSS Protection**: Go template automatic escaping
- **No Authentication**: Read-only dashboard (no sensitive operations)
- **CORS**: Not needed for same-origin requests

### Future Enhancements

Potential improvements for the webapp:

1. **Real-time Updates**: WebSocket integration for live data updates
2. **Filtering**: Date range and newspaper filtering options
3. **Export Features**: CSV/PDF export of data and charts
4. **Search**: Full-text search across articles
5. **Caching**: Redis integration for frequently accessed data
6. **Authentication**: User management if needed for private deployment
7. **API Documentation**: Swagger/OpenAPI documentation
8. **Monitoring**: Health checks and metrics endpoints

### Deployment Notes

The webapp is designed to be deployed alongside the existing Python application:

- **Port**: Runs on port 8080 (configurable)
- **Database**: Uses the same SQLite database as the Python app
- **Static Files**: Served via CDN (no local static file serving needed)
- **Process Management**: Can run as a separate service or container
- **Resource Usage**: Minimal memory footprint (~10-20MB)

This Go webapp provides a modern, performant alternative to the existing Python dashboard while maintaining full compatibility with the existing database structure and data.