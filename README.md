# PythonRADIUSCheck

A simple check to see if Replication is lagging or not. Checks for most recent entry in  
the radpostauth table, compares it to current date and time.  
This could be updated to compare it to the original DB for more accuracy,  
but in our case radpostauth moves quick enough that this test is accurate enough.
