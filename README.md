# Cargo Service

#### Credentials for demo:

> You can register to test the functionality using any valid email, 
> no special credentials are required. A certain amount of money will 
> be immediately added to your account for testing.


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

on the manufacturers page you can see information about each manufacturer
![manufacturers](images_for_readme/manufacturers.JPG)

we can also go to the detailed page and see which cars are available
![manufacturer_details](images_for_readme/manufacturers_details.JPG)

on the truck detailed review page, we can rent the truck we like, the money will be debited from the account immediately
![rent](images_for_readme/rent_now.JPG)

we will also see info about it in the sidebar, and a message at the top right (all successful or unsuccessful actions 
are accompanied by messages)
![rent_success](images_for_readme/rent_success.JPG)

Now we can go to the orders page. All requests differ in color and status, some are already being 
fulfilled by other drivers. We can choose from green (available)
![orders](images_for_readme/orders.JPG)

Let's go to the orders page and select one that we want to take. As we can see, this order weighs more 
than our car can afford.
![order_not_avaliable](images_for_readme/order_not_avaliable.JPG)

So, let's try something else that's not so difficult. Now we can see the current order in the sidebar 
and the driver's detailed page.
![driver_with_order](images_for_readme/driver_detail_with_order.JPG)

after completing the order, click "complete", and as we can see, the funds have been credited to the balance
![completed](images_for_readme/order_completed.JPG)

On the services page you can see all the truck's maintenance services.
![services](images_for_readme/services(empty).JPG)

We can create a service by selecting an option from the drop-down list.
![create_service](images_for_readme/create_service.JPG)

After the service is created, we can see that it has been added to the list, and the car's condition has improved by the corresponding percentage.
![service_success](images_for_readme/service_cuccess.JPG)
