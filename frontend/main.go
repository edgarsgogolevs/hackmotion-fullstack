package main

import (
	"log"
	"net/http"
)

const PORT = ":8080"

func main() {
  http.Handle("/", http.FileServer(http.Dir("web")))
  log.Printf("Serving at %v", PORT)
  log.Fatal(http.ListenAndServe(PORT, nil))
}
