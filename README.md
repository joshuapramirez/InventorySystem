# Inventory System
Inventory Management System for Businesses/Sellers


## Table of Contents
- [Description](#Description)
- [Features](#Features)
- [Installation](#Installation)
- [How to run](#How-to-run)
- [Distinctiveness and Complexity](#Distinctiveness-and-Complexity)
- [Files](#Files)


## Description
I have developed an inventory management system tailored to support businesses and sellers in meticulously tracking their inventory and sales activities. The user-centric interface offers seamless interaction, enabling effortless updates to inventory and seamless addition of sales transactions. Through intuitive graphical representations, users can visually grasp the performance of their products, aided by dynamic graphs. Additionally, the system streamlines product search and access within the available stock, enhancing operational efficiency.


## Video Walkthrough
[Watch the Video Walkthrough](https://youtu.be/9AFGgIo1nNA)

In this video, I go through the features and functionality of this project.


## Features
- User Account Creation
- Effortless Product Addition
- Streamlined Product Updates
- Efficient Product Deletion
- Interactive Sales Tracking
- Comprehensive Product Insights
- Intelligent Product Search
- Search Suggestions
- Visual Performance Analytics

### Installation
pip3 install django
pip install django-pandas
pip install plotly


### How to run
1. cd inventorySystem
2. python manage.py runserver

## Distinctiveness and Complexity
This project stands out due to its unique approach and intricate design. The primary focus is on real-time manipulation of inventory data within a responsive web application. The application employs modal components to facilitate dynamic data modifications within charts without requiring a page refresh. Additionally, the data is visually represented through graphs, enhancing user comprehension.

The utilization of modals is a recurring theme throughout the project. They serve various purposes, including chart manipulation, search form recommendations, and confirmation dialogs for inventory deletion. This strategic incorporation of modals significantly enhances the user experience. Furthermore, the application's responsiveness to varying screen sizes ensures content remains organized and visually appealing.

The project's complexity is pervasive, spanning across various technical domains. Achieving seamless integration between HTML, JavaScript, CSS, and modal components posed a noteworthy challenge. Particularly intricate was the implementation of the central chart feature, enabling users to effect changes directly without reloading the webpage. Overcoming hurdles associated with modal-button interactions was complex, albeit relatively more manageable compared to the central chart integration.

A significant technical challenge arose when transmitting parameters through modals, views.py, and JavaScript. Unexpected bugs continually emerged, with each solved issue seemingly giving rise to new complications. Moreover, ensuring responsive design through CSS proved demanding. The task of enabling graphs to adapt dynamically to different screen sizes was more intricate than initially anticipated. Remarkably, this challenge was surmounted by employing the Document Object Model (DOM) to detect screen size changes and subsequently invoking a function to generate new graphs as required.

Summing up, I believe this project truly shines through its unique attributes, complexity, and the technical obstacles I've navigated. The meticulous integration of diverse technologies and my adept handling of intricate challenges showcase my skills and unwavering commitment to providing users with a polished and seamless experience.


## Files
- forms.py - Contains forms for adding products and updating inventory records.
- models.py - Defines the Inventory model, facilitating storage of product data.
- views.py - Implements Python functions for various operations, including adding, updating, deleting, and searching products. It also manages graph creation and modal functionality.
- urls.py -  Manages all application URLs.
- dashboard.html - Presents graphical representations of product performance.
- empty_inventory.html - Informs users of zero products and offers a button to redirect to the product addition form.
- inventory_add.html -  Form for adding new products to the inventory.
- inventory_update.html - Form for updating existing product details.
- inventory_list.html - Main application page displaying a chart with comprehensive product information and manipulation options.
- layout.html - Provides the overall application layout.
- per_product.html - Individual product-specific page.
- login.html - User login page.
- logout.html - Notifies users upon logout with a link to the login page.
- register.html - User account creation page.
- style.css - CSS defining the application's base appearance.
- search_and_delete.css - CCSS handling styles for the search and delete confirmation modals.
- dashboard.js - JavaScript functions responsible for graph rendering.
- delete_confirmation.js - JavaScript facilitating the functionality of the delete confirmation modal.
- inventory_list.js - JavaScript enabling modal interaction, stock quantity updates, and transaction recording.
- search.js - JavaScript powering the search modal and search form.
- admin.py - Facilitates the administration interface for managing application data models.
- settings.py - Contains configuration settings for the Django project. It includes settings for database connections, middleware, templates, authentication, internationalization, time zones, and static files handling.
