# Cargo Service

#### Credentials for demo:

> Username: Demouser
> 
> Password: 1qazcde3

Cargo Service is a Django-based web application for managing cargo transportation.
Drivers can rent trucks, take available orders based on truck capacity, and track order status in real time.
The project focuses on clear business logic, data consistency, and practical backend architecture.

## Quick start


```shell

1. Clone project `git clone https://github.com/AngryAndrii/cargo-service.git`.
2. Create and activate virtual environment.
3. Install requirements `pip install requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Load the dumped data back to database: `python manage.py loaddata dump.json`
6. Run the project: `python manage.py runserver`
```

## Application functionality

After entering the site, we find ourselves on the login page.
![entert](images_for_readme/1.jpg)

Log in to the sites using demo user data
> Username: Demouser
> 
> Password: 1qazcde3

![login](images_for_readme/2.jpg)

After that we can go to trucks page to rent a car. 
The list of cars is displayed in 5 pieces, and with loading via a button
![carlist](images_for_readme/3.jpg)

we can rent any car if it is not occupied by another driver, in which case we will get an error
After that, in sidebar we can see our rented truck, and our just get smoller (with a transaction)
![rent car](images_for_readme/4.jpg)

Now we can go to the orders page. All requests differ in color and status, some are already being 
fulfilled by other drivers. We can choose from green (available)
![car_rented](images_for_readme/5.jpg)

Oh, great order, metal rails. But what is this? The weight is almost 30 tons, and our truck is designed for less. 
When you try to take this order, an error message will be displayed.
![heavy_error](images_for_readme/heavy_error.jpg)

So let's choose something easier. After receiving the order, we see a message, and its display in the sidebar
![order_took](images_for_readme/taked_order.jpg)

Now we will assume that we have completed the order, click the completed order button 
(by the way, confirmation of all actions occurs through modal windows)
![complete_order](images_for_readme/complete_order.jpg)
The order goes into the completed status, and money is added to our account, this is visible in the sidebar
![complete_succes](images_for_readme/complete_order_succesfull.jpg)

The service book page displays information about all car maintenance. Let's say you performed it at a service station, 
and you can enter the data here using a convenient form.
![repair](images_for_readme/repair.jpg)

after confirmation, the entry is added to the list of all repairs. Money is not debited. since the work was 
carried out separately from our platform
![repair_complete](images_for_readme/repair_complete.jpg)

Let's say we decide to return the track. To do this, click on the return button in the sidebar.
![return_truck](images_for_readme/return_truck.jpg)

Track successfully returned
![truck_returned](images_for_readme/truck_returned.jpg)
