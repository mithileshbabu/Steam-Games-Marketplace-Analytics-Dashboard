# Steam Games Marketplace Analytics Dashboard

## Project Overview

This project analyzes the Steam Games Marketplace dataset to identify trends in game releases, pricing, discounts, developers, publishers, game tags, and supported languages. The analysis was performed using Python in Jupyter Notebook with interactive visualizations.

## Objectives

- Clean and preprocess the dataset.
- Perform exploratory data analysis (EDA).
- Answer analytical questions using data visualization.
- Identify patterns and trends in the Steam marketplace.

## Note

The notebook is best viewed and executed in **Jupyter Notebook** or **Visual Studio Code (VS Code)**.

Interactive Plotly visualizations may not be displayed directly on GitHub due to GitHub's notebook rendering limitations. However, all charts and outputs are available when the notebook is opened and executed in Jupyter Notebook or VS Code.

## Dataset

The dataset contains information about Steam games, including:

- Game Title
- Original Price
- Discounted Price
- Release Date
- Developers
- Publishers
- Popular Tags
- Supported Languages
- Reviews

## Technologies Used

- Python
- Pandas
- NumPy
- Plotly
- Jupyter Notebook

## Analytical Questions

1. How has the number of game releases changed over the years?
2. How are games distributed between free and paid titles?
3. What is the distribution of game prices?
4. How are discount percentages distributed?
5. Which developers have published the most games?
6. Which publishers have published the most games?
7. Which months have the highest number of game releases?
8. What are the most common game tags?
9. Which languages are most commonly supported?
10. Is there a relationship between original price and discounted price?


## Key Findings

- Most Steam games are paid titles.
- Most games are priced below $200.
- Game releases vary throughout the year.
- A few developers and publishers dominate the marketplace.
- Action and Adventure are among the most common game tags.
- English is the most widely supported language.
- Discounted prices generally increase with original prices.

## Repository Structure

```
Steam-Games-Marketplace-Analytics-Dashboard
│
├── data
│   └── merged_data.csv
│
├── images
│   ├── dashboard_home.png
│   ├── release_trend.png
│   ├── top_developers.png
│   └── scatter_plot.png
│
├── notebook
│   └── analysis.ipynb
│
├── app.py
├── README.md
├── requirements.txt
```

## How to Run

1. Clone the repository.
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Open `notebook/analysis.ipynb` in Jupyter Notebook or VS Code.
4. Run all cells to reproduce the analysis.
