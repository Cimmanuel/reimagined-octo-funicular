.DEFAULT_GOAL := welcome

welcome:
	@echo "Welcome! Take a look at the file and select an actual target"

scrapeinsta:
	@echo "Crawling sequence initiated..."
	@cd instacrawl/instacrawl/spiders && scrapy crawl instaspider
