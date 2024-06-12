# Design Concept:
**I chose a white background and simple colours to ensure elements are visible and users can easily identify important information. Buttons and important information are highlighted in simple green or blue as well. Key elements like forms and tables are placed in containers with shadows, making them distinct against the white background and allowing users to focus and identify them easily. This design approach provides a comfortable experience for users. Additionally, I aimed to create a clean and simple design, differentiating elements using neutral and other colours.**


## Main Page:
I centred the welcome message card with padding to create a modern and clean design. The main page features a navigation bar and a large central welcome message card. Clicking the company name at the top routes the user back to the main page, ensuring they can always return to the main screen. 

## Booking Page:
 This page uses a light grey background at the top to indicate its purpose to users. The button is blue, contrasting with the neutral tones to make it easy to find. Instead of using radio buttons for selecting campsites, I decided to use a dropdown element for campsite selection to save space and maintain a consistent look with the customer name element.

## Camper List:
The camper list is displayed in a table format, which is ideal for showing information about many campers. The title "Camper List" at the top explains the page, and the table headers are in bold and light blue to separate them from the table body. All text is centre-aligned for better readability. I applied a hover effect with a dark grey background on table rows to enhance the user experience and clarity.

## Customer List:
I decided to divide the page into three main sections: a search bar with a title at the top, an "Add Customer" button in the middle, and the customer table at the bottom. This structure is common in many customer management sites. The search bar includes a search icon and button to indicate its purpose, and the "Add Customer" button aligns with the table action row for consistency.

## Report:
I used the same table style for the report page to ensure design consistency across all pages.

## Validation:
form validation is implemented using Bootstrap's "required" attribute to ensure all fields are completed. The phone number field is validated on the server side using regular expressions to match New Zealand's phone number rules (9-10 digits). Because this rule can be customised to New Zealand's specific format, I decided to use server-side regular expressions for validation. If the input doesn't match the regex, an error message is shown.

## Router:
I named server handlers to closely match URLs, making it easier for other developers to understand the code. The routing names are closely aligned with the URLs. For example, the server handler for "/customer" is named customerlist(), which increases readability for other developers. URLs clearly indicate the request, such as "/customer/result" showing search results for customers.

## Confirmation and Redirection:
I included confirmation pages with redirection links to clearly indicate the server's response to user actions, enhancing the user experience. Responses to actions like customer bookings and information changes are shown on a confirmation page. Links for redirection to the main page are included, ensuring the server's response to user actions is clear and improving the user experience through confirmation.

## Flex : 
I decided to use the flex system in Bootstrap because many elements on this website need to be aligned with parent elements or other components. The attributes “d-flex,” “justify-content-center,” “align-items-center,” and “align-content-center” provide perfect alignment solutions.

## Get, Post:
I used the GET and POST methods to read booking and customer data from the database, as well as to update or insert customer information into the database. These methods are standard practices for handling HTTP web requests.



# Database Question


## 1.   What SQL statement creates the customer table and defines its fields/columns? 
```
CREATE TABLE IF NOT EXISTS `customers` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(45) NULL,
  `familyname` VARCHAR(60) NOT NULL,
  `email` VARCHAR(255) NULL,
  `phone` VARCHAR(12) NULL,
  PRIMARY KEY (`customer_id`)
);
```

## 2.   Which line of SQL code sets up the relationship between the customer and booking tables?

```
CREATE TABLE IF NOT EXISTS `bookings` (
  `booking_id` INT NOT NULL AUTO_INCREMENT,
  `site` CHAR(3) NULL,
  `customer` INT NULL,
  `booking_date` DATE NULL,
  `occupancy` INT NULL,
  PRIMARY KEY (`booking_id`),
  INDEX `site_idx` (`site` ASC) VISIBLE,
  INDEX `customer_idx` (`customer` ASC) VISIBLE,
  CONSTRAINT `site`
    FOREIGN KEY (`site`)
    REFERENCES `scg`.`sites` (`site_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `customer`
    FOREIGN KEY (`customer`)
    REFERENCES `scg`.`customers` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);
```

## 3.   Which lines of SQL code insert details into the sites table?

```
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P1', '5');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P4', '2');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P2', '3');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P5', '8');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P3', '2');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U1', '6');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U2', '2');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U3', '4');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U4', '4');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U5', '2');
```

## 4.   Suppose that as part of an audit trail, the time and date a booking was added to the database needed to be recorded. What fields/columns would you need to add to which tables? Provide the table name, new column name and the data type. (Do not implement this change in your app.)

```
table name: Bookings
column name: CreatedAt
data type: DATETIME
```

## 5. Suppose the ability for customers to make their own bookings was added. Describe two different changes that would be needed to the data model to implement this. (Do not implement these changes in your app.)

I should create a new booking table for customers and build relationships with the original booking table using foreign keys.
```
Create new table:  BookingFromCustomer
BookingID-Foreign key to Booking table (INT)
CustomerID- Foreign key to Customer table (INT)
SiteID, -Foreign key to Site table(INT)
BookingDate – DATETIME 
```

Also need to add authentication to customer table 
```
Table: Customer
Authentication – VARCHAR(50)
```
So only customer who has authentication, can create booking and access.
