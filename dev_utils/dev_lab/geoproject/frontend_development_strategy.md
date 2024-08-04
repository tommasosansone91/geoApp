# frontend development strategy

when developing the frontend part,
first we develop things in the standalone folder `geoproject`.

When they are tested to work, 
- we copy the html files into the django project in folder `templates` (`/geoApp/static`).
- we run `python manage.py collectstatic` to copy the static files (js, css, font, images) into the django project in folder `static` ( `/geoApp/static`).

we leave the source components in `geoproject` .