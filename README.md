# good-stoop

Dashboard to visualize any issues in various parts of NYC

## Data Sources
- [NYC Restaurant Inspection data](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j)
- [Department of Buildings Complaints Received](https://data.cityofnewyork.us/Housing-Development/DOB-Complaints-Received/eabe-havv)
- [Borough Boundaries](https://data.cityofnewyork.us/City-Government/Borough-Boundaries/tqmj-j8zm)
- [NYPD Complaint Data](https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Current-Year-To-Date-/5uac-w243)

## Goal
Dashboard of a NYC heat map showing which areas have more complaints than others. Restaurant view will show areas where restaurants have low or high inspection results.

## To Run

1. Install packages `npm install`
2. Start reactjs webserver `yarn start`
3. Create python venv inside api dir `api $ python3 -m venv venv`
4. Activate venv `source venv/bin/activate`
5. Install python packages listed in api/requirements.txt `(venv) $ pip install flask ...`
6. Start flask api `yarn start-api`

## TODOs
- [ ] create queries to get borough boundaries
- [ ] create queries to get complaint data for each borough boundary
- [ ] create queries to get complaint data for individual locations
- [ ] create queries to get restaurant data for each borough boundary
- [ ] create queries to get restaurant data for individual locations
- [ ] create dashboard with react

Created with: https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project