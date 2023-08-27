function createPlotlyChart(containerId, graphData) {
    Plotly.newPlot(containerId, graphData, {});
  }

  // Initial chart creation
  createPlotlyChart("chart1", dailyProductSalesGraph);
  createPlotlyChart("chart2", highestSalesGraph);
  createPlotlyChart("chart3", mostSoldProducts);
  createPlotlyChart("chart4", mostProductInStock);

  // Attach window resize event listener to adjust chart size
  window.addEventListener("resize", function() {
    createPlotlyChart("chart1", dailyProductSalesGraph);
    createPlotlyChart("chart2", {{ highest_sales_graph| safe }});
    createPlotlyChart("chart3", {{ most_sold_products| safe }});
    createPlotlyChart("chart4", {{ most_product_in_stock| safe }});
  });