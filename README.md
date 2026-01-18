# Cargo Service

#### Credentials for demo:

> Username: Demouser
> 
> Password: 1qazcde3

Cargo Service is a Django-based web application for managing cargo transportation.
Drivers can rent trucks, take available orders based on truck capacity, and track order status in real time.
The project focuses on clear business logic, data consistency, and practical backend architecture.

## Diagram

![scheme](images_for_readme/scheme.JPG)


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
![entert](images_for_readme/Enter.JPG)

Register to the site or login if you've already registered  
***after registration you should login!***

![login](images_for_readme/register.JPG)

after that we will be on the main page

![welcome](images_for_readme/welcome.JPG)

After that we can go to trucks page to rent a car. 
The list of cars is displayed in 5 pieces, and with loading via a button

![trucks](images_for_readme/trucks.JPG)

On the driver page we can see list of drivers

![drivers](images_for_readme/drivers.JPG)

you can also go to the detailed driver review page

![driver](images_for_readme/driver_detail.JPG)



![driver_with_order](images_for_readme/driver_detail_with_order.JPG)
![manufacturers](images_for_readme/manufacturers.JPG)
![manufacturer_details](images_for_readme/manufacturers_details.JPG)
![completed](images_for_readme/order_completed.JPG)
![order_not_avaliable](images_for_readme/order_not_avaliable.JPG)
![orders](images_for_readme/orders.JPG)
![rent](images_for_readme/rent_now.JPG)
![rent_success](images_for_readme/rent_success.JPG)


![create_service](images_for_readme/create_service.JPG)

![services](images_for_readme/services(empty).JPG)

![service_success](images_for_readme/service_cuccess.JPG)



we can rent any car if it is not occupied by another driver, in which case we will get an error
After that, in sidebar we can see our rented truck, and our just get smoller (with a transaction)
![rent car](images_for_readme/4.JPG)

Now we can go to the orders page. All requests differ in color and status, some are already being 
fulfilled by other drivers. We can choose from green (available)
![car_rented](images_for_readme/5.JPG)

Oh, great order, metal rails. But what is this? The weight is almost 30 tons, and our truck is designed for less. 
When you try to take this order, an error message will be displayed.
![heavy_error](images_for_readme/heavy_error.JPG)

So let's choose something easier. After receiving the order, we see a message, and its display in the sidebar
![order_took](images_for_readme/taked_order.JPG)

Now we will assume that we have completed the order, click the completed order button 
(by the way, confirmation of all actions occurs through modal windows)
![complete_order](images_for_readme/complete_order.JPG)
The order goes into the completed status, and money is added to our account, this is visible in the sidebar
![complete_succes](images_for_readme/complete_order_succesfull.JPG)
