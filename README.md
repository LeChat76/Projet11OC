<p align="center">
    <img alt="logo" src="https://github.com/LeChat76/Projet10OC/assets/119883313/881f780c-7907-4f44-b294-7c3bb0b66dda">
</p>

# Projet11OC
Debugging and testing web application coded with Flask.

## Installation
* Clone repository: `git clone https://github.com/LeChat76/Projet11OC.git`  
* Enter in created folder: `cd Projet11OC`  
* Create virtual environment: `python -m venv .venv`  
* Activate environment:  
    * for Linux `source .venv/bin/activate`  
    * for Windows `.\.venv\Scripts\activate`  
* Access to the branch who contain the latest update : `git checkout QA`
* Install the necessary libraries: `pip install -r requirements.txt` 
* Run the webserver : `python .\server.py`  

## Many issues have to be debugged, bellow list of them:
* Error "Entering a unknown email crashes the app":
  * Description : when entering an inval email to login, app crash
  * Why this issue : the request used to select account associated to the email provided return None when no account associated
  * Resolution : adding function to search club associated to email provided. If no => display warning message
  * branch : https://github.com/LeChat76/Projet11OC/tree/error/Entering_a_unknown_email_crashes_the_app
* Bug "Clubs should not be able to use more than their points allowed":
  * Descrition : when a club purchase places for a competition, if the club have not enough points, purchase is done anyway (and amount of points become negative!)
  * Why this issue : no check of amount point of the club who purchase places
  * Resolution : adding the condition "if" amount of point is enough to purchase places, if not => display warning message
  * branch : https://github.com/LeChat76/Projet11OC/tree/bug/Clubs_should_not_be_able_to_use_more_than_their_points_allowed
* Bug "Clubs shouldn't be able to book more than 12 places per competition":
  * Description : a club must not purchase more than 12 points
  * Why this issue : noting coded to prevent purchase of more than 12 places
  * Resolution : adding tag max="12" in HTML page. In that way, unable to enter more than 12 places to purchase
  branch : https://github.com/LeChat76/Projet11OC/tree/bug/Clubs_shouldnt_be_able_to_book_more_than_12_places_per_competition
* Bug "Booking places in past competitions":
  * Description : a club must not be able to purchase places for a dated competition
  * Why this issue : nothing coded to check date of competition purchased
  * Resolution : adding the condition "if" date of competition purchased is inferior to now => display warning message
  * Branch : https://github.com/LeChat76/Projet11OC/tree/bug/Booking_places_in_past_competitions
* Bug "Point updates are not reflected":
  * Description : when purchase places of competition, amount of point of the club remain the same
  * Why this issue : no calculation of remain point after purchasing
  * Resolution : adding calculation "current point" - "purchased point"
  * Branch : https://github.com/LeChat76/Projet11OC/tree/bug/Point_updates_are_not_reflected
* Feature : "Implement Points Display Board":
  * Description : users need to access to an board with all places available for all competitions, no need to login to access to this feature
  * Resolution : added http link to this feature from homepage and create a new html page with board and shade of grey for improved readability
  * Branch : https://github.com/LeChat76/Projet11OC/tree/feature/Implement_Points_Display_Board
* Personnal debugging:
  * no reflection in json file : adding function to write data to json file
  * adding confirmation message when purchasing places (adding number of places purchased and for which competition)
  * prevent purchasing more place than available in competition
  * adding min value for purchase (min=1 because it's just logic ;-))
  * Branch : https://github.com/LeChat76/Projet11OC/tree/feature/Personnals_features