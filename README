Wisconsin Herbarium Google App Engine Python README

This file discusses how to create the Wisconsin Herbarium  
running in a local Google App Engine.  If you have the 
large data files, you can build and run the entire 
application locally.  The web client files which 
populate the datastore work locally and with the real 
Google App Engine.  You'll need to edit the host line 
inside formPOSTspecies.py and formPOSTspecimen.py to 
point them to the live Google App Engine instance that 
you create.  In real testing, the formPOSTspecies.py and 
formPOSTspecimen.py web clients (running on your machine) 
consume an enormous amount of the free allotment of 
resources.  They work fast enough but the "DataStore 
writes" limit reaches 100% in a very short time and only 
less than 500 Species kind records can be inserted in one 
day.  At that rate, it would take 40 days.  A similarly 
slow rate would take the Specimen kind about 2 years.  
It seems to me that nothing is wrong with the web clients 
or the application that causes too much consumption.  It 
is simple and standard HTTP POSTing to a normal web app.  
Therefore, some kind of batch uploading will be necessary 
because locally grown datastores cannot be uploaded.  This 
has not been investigated carefully.  The Wisconsin 
Herbarium should only be running at its home at 
www.botany.wisc.edu/herbarium/ anyway.  Rewriting it to run  
on Google App Engine is experimental activity and should 
be done only with "Admin-login" access setup in app.yaml. 
Otherwise it will end up in Google searches. Alternatively, 
datastore writing could be sped up by having someone
pay Google and increase the 
"Datastore writes" limit.  Rumor has it that setting up 
a credit card alone increases the free limit (even without 
allocating any payment).  It should be easy to set a 
limit (of say $10 per day) to see how much it would cost 
to populate the Datastore with all of the data.  It would 
be best to increase the quality of the code before doing 
so.  Testing might reveal some shortcomings of the 
Datastore design.  In particular, there's nothing for 
blobstore images.  Also, the "view" is completely bare.  The 
view is easy to change very quickly.  Datastore design 
problems should be the focus and might prevent having to 
get(), change and put() every entity.  

The "join" between the two kinds, Species and Specimen, is 
carried out in the standard way for one-to-many, where one 
Species has many Specimens.  All of the properties in both 
kinds are like this:

cat /usr/local/herb18/models.py |grep Property|sed 's/.*db\.//'|sort |uniq

ReferenceProperty(Species)
StringProperty(default="")
StringProperty(default="", multiline=True)
TextProperty(default="")

...a better model would make more use of "correct" properties 
for dates and integers.  This would involve an unknown 
amount of data massaging.  Remember, the data being used 
is text files from mysqldump.  Putting everything into 
StringProperty() has the benefit of not having to massage 
the incoming data.  It has only the cost of having to write 
additional code to translate string dates and numbers into 
usable objects in python.  Because data entry is performed 
by Herbarium personnel using an HTML form talking to a normal 
web application (at www.botany.wisc.edu/herbarium), the 
massaging would be an ongoing process.  Instead, with only 
StringProperty(), it could be directly used for migration into 
AppEngine.  Notice the StringProperty(default="", multiline=True) 
and TextProperty(default="").  They are discussed below and may 
have to be addressed with data massaging.  Back to the kinds 
Species and Specimen whose relationship is one-to-many.  This 
relationship is managed in model.py by the single ReferenceProperty 
which is in the kind Specimen, each of which has one of these:

ReferenceProperty(Species)

...inside of main.py AddSpecimenHandler.post(), we create the Specimen entity 
like this excerpt shows.  Notice that we query for the species object 
that we will use for the Specimen ReferenceProperty.  Then we make 
the Specimen:

queryResults = models.Species.all().filter("Taxcd =", speciesTaxcdASN)
species = queryResults.get()
specimenInstance = models.Specimen(ACCESSION = self.request.get('ACCESSION'),
    TYPE = self.request.get('TYPE'),
    ...
    ...
    DTRS = self.request.get('DTRS'),
    species = species)

Notice that the species property is type ReferenceProperty(Species) and can 
be populated with instances of entities of kind Species, which is what 
we are doing here for every post(), after retrieving the correct (already 
existing) Species entity using the query with the filter. 
If the web clients formPOSTspecies.py and formPOSTspecimen.py are used 
to populate the datastore, then all of the Specimen entities will have 
a reference to its Species entity.  This is the reason why you must 
populate the Species first--so that the query shown above returns a 
record.  Because this depends on the quality of the data, careful 
attention needs to be paid to whether a Species is always returned by 
that query.  The existing web application uses field data to model the 
one-to-main species-to-specimen relationship.  The actual SQL query does 
something like this:

SELECT * FROM specimen INNER JOIN species ON specimen.TAXCD = species.Taxcd WHERE...

This same logic can be performed in AppEngine.  But the AppEngine way 
would be the standard way, given the modeled relationship show above:

species = db.get(species_key) ##(specimen is an instance of Species)
for specimen in species.Specimen_set:
    #specimen is a Specimen instance

In this way, we can use the Species automatic back-references to find 
the related Specimen entities.  Specimen_set is the default name of the 
collection (name of the referring class followed by "_set"). 

The programs work good and local population on a small 
PC takes about a day and about 5 gigabytes.  Populating the Species 
takes about an hour and populating Specimen (which queries Species AND 
put()s the Specimen) 300,000+ times, takes a day on a local machine. 


Apparently the --use_sqlite option isn't understood by dev_appserver.py 
anymore and is the default.  Otherwise, these aging notes 
should work with current Google App Engine SDKs:


You can start the server on port 80 like this:

python /usr/local/google_appengine/dev_appserver.py --use_sqlite --datastore_path=/home/knoppix/dev_appserver.datastore herb18

...notice that dev_appserver.datastore is a (possibly existing) sqlite3 database of the datastore. 
If it doesn't exist, then you'll have to populate it first.  
The homepage is here:
http://localhost:8080/
The admin page is here:
http://localhost:8080/_ah/admin
The entire application exists in main.py and models.py. 
There are other template-related files that are static but required, like _base.html, count.html
Populating the datastore is not easy.  If you have a pre-populated datastore in 
dev_appserver.datastore, then you're good to go.  This database will be written to if you add or 
update records by manipulating in _ah/admin.  This database is probably also written to when 
simply using the application, to keep statistics and other things.  This database is 4.7gigs 
large even though it was populated with small (103MB) data files:
 4.8M Jun  8 /home/knoppix/herb18/spdetail_herbfortynine13.txt
 98M Jun 10 /home/knoppix/herb18/specimen_herbfortynine1.txt
These two files can be used to populate the datastore.  Inside main.py, there are two handlers 
for inserting records.  These can be populated by visiting a web page with your web browser 
and filling out the form and clicking submit.  The form comes from the get() method in these 
two handlers:
AddSpecimenHandler
AddSpeciesHandler
...and those same handlers have post() methods which take the filled out form and create a 
record in the datastore.  The two models, Species and Specimen, are defined in models.py. 
The two text-dump files: 
 spdetail_herbfortynine13.txt
 specimen_herbfortynine1.txt
...contain all of the data for Species and Specimen.  These two files can be read by two programs:
formPOSTspecies.py
formPOSTspecimen.py 
...by running them in the same directory as the text files, like this: 
python formPOSTspecies.py
python formPOSTspecimen.py 
...and they must be done in that order.  formPOSTspecies.py takes less than an 
hour to run but formPOSTspecimen.py takes about a day.  It doesn't finish because it
barfs on a bad record (multiline LAT value).  But it does insert almost every record 
because more than 349,000 records successfully get entered.  You can see in models.py 
several fields that declare-as-okay "multiline=True".  The LAT property will also need 
that if it would finish.  Almost all of the multiline=True are probably not necessary 
but there are newlines in strange places.  The text files were dumped from a mysql 
database but both ended up with too many delimiters in some records and these records 
were simply deleted--we are only talking a small number of records <100 in all.  Therefore,
to insert every record will require massaging (removing vertical-pipe values in data, for 
example).  Another problem is that DS values that can be indexed, like StringProperty, 
cannot be larger than 500 bytes.  Some Specimen property values, like HABITAT, could be 
expected to exceed 500 bytes.  And as the source is mysql varchar() type, the actual data 
can be over 500 for any columns.  These rows too, were deleted, when they shouldn't have 
exceeded 500 bytes.  For example, if SITENO was over 500bytes, then something was wrong 
with that row.  It was deleted.  Other properties, like HABITAT, were changed to a 
different DS type, like TextPropery, which can exceed 500 bytes.  See the larger-than-500 
by looking in models.py to find properties with TextPropery.  Similarly, see models.py to 
see which fields have at least one record with a multiline condition.  The short story is 
that these mysql-dumps-to-text contain almost all of the records and can almost all be 
inserted into the Datastore by running the 2 web client programs with the 2 text files in 
the current directory.  Massaging the data will allow more of the few currently-un-insertable 
rows go in.  Recall that we said that the Species entities must be created first, like this:
python formPOSTspecies.py
...that is because when, later on, you insert the Specimen records, like this:
python formPOSTspecimen.py 
...something much different happens.  AddSpecimenHandler.post() actually runs a query to find 
the one "parent" or "owning" Species record.  It inserts this as a ReferenceProperty(Species) 
into the currently-being-created Specimen entity.  Every Specimen should have one value in the
ReferenceProperty that points to a Species entity.  This achieves the one-to-many relationship 
so that every Species can have many Specimens.  This allows the very elegant and efficient 
backreferencing system to work.  This allows us to quickly find all of the Specimens for a 
given Species.  This same effect could have been achieved like it is in SQL where we find like so: 
SELECT * FROM specimens WHERE specimen.TAXCD == species.Taxcd AND species.Syn='.'
If you want to redo the formPOSTspecies.py formPOSTspecimen.py inserts, then you'll need a whole 
day and 4.7GB of free space.  You'll want to start the dev_appserver by first clearing the DS.  
You might want to save the existing DS first:

mv /home/knoppix/dev_appserver.datastore /home/knoppix/dev_appserver.datastore.BACKUP 

After you took your backup, you can just start the dev_appserver in the normal way:

python /usr/local/google_appengine/dev_appserver.py --use_sqlite --datastore_path=/home/knoppix/dev_appserver.datastore herb18

...and it will notice that it needs to create the dev_appserver.datastore sqlite3 database. 
You can also start it by clearing the existing datastore, like this:

python /usr/local/google_appengine/dev_appserver.py --use_sqlite --datastore_path=/home/knoppix/dev_appserver.datastore WRONG-cBECAREFUL herb18

...notice that you should be careful with the "-c" clear database because it will delete the file. 
This can cost you an entire day of time and 4.7GB of data. 
Because the creation of a Specimen entity requires a datastore query, it is slow.  It needs to 
find the existing Species entity to create its Specimen.species ReferenceProperty value.  

...notice that only Species and Specimen are created.  Other tables are used by the classic 
web application including, at least, t_vascular_common_names early on, habitat and link for 
the species detail page.  And also from tables sitelkup, colleventlkup, annlkup, later on.

These extra tables have some content to make a few items of content in the classic webapp.  

To use the database, just fire it up with dev_appserver.py and visit the homepage:
http://localhost:8080/
From there you can browse via Family or Genus and drive all the way to the specimen. 
