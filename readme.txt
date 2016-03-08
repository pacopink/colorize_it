========= General Information ==========
I am analyzing msg trace files that containse with multiple dialogs/transactions for a single call session in plaint txt file.
It is crazily difficult to keep track on each transaction in mind while reading it in plaint text mode.
So I develop this webapp based from python flask to upload my message trace file, and automatically recognize the type,
then select a suitable parser to: 
1. parse the message trace into message blocks.
2. categrize each blocks' category and subtypes
3. transform all blocks with categroy and subtypes as the tag as part of the html to response
4. response the transformed msg tag along with the referenced css

After client browser get those response, it will render each message block via the tag, according to the css,
in this way, a colorized msg trace can be retrieved.

2016-3-8
enhance the GUI
some javascripts are added to filter via message categories

========= Usage ==========
Assume that you have python and flask in place,
simply run run.sh to get it started, listening on '0.0.0.0:5050', with DEBUG flag on,
you can change these settings from colorize.py.

Use your browser to visit 'http://<you host>:5050/'

========= Customzation ========
You can define your own parser via overriding BaseDocument.parse, BaseBlock.get_category and BaseBlock.get_subtype,
just like what ocg_parser.py and ct_parser.py do.
and register them to parser_map in render.py.
The 3 element in a parse tripple in parser_map stands for ['re filename pattern', 'document instance', 'file type name'] 
the static/style.css can also be customized to whatever color scheme you like, new tags can also be added.
Just remember to force your browser refresh the css via visit http://<your host>:5050/static/style.css with a Ctl+F5, once you update the css.

======== Illustration =======


     +---------------------+
     | colorize.py         |
     |                     |               you can wirte your parser
     +----------+----------+               like these 2, and register
                |                          to render.py 
                |call                           |   |
                v                               v   |
     +---------------------+            +-------+-------+            +----------------+
     | render.py           |   use      | ocg_parser.py |   impl     |base_parser.py  |
     |                     |----+------>|               |-----+--->>>|                |
     +----------+----------+    |       +---------------+     |      ++---------------+
                |               |                   |         |
                |               |                   v         |
              refer             |       +---------------+     |
                |               |       |ct_parser.py   |     |
                |               +------>|               |-----+
                |                       +---------------+
                v
     +---------------------+
     |static/style.css     |
     |                     |
     |                     |
     +---------------------+

