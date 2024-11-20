# NYT dot WTF

weekend project to build an automated solver for the [NYT games page](https://www.nytimes.com/crosswords), partly inspired by the existence of the .wtf tld.  

notably:

- the nyt has two different flavors of endpoints from which you can extract solutions.  for the easy one, you can include the solution date that you want as part of the URL and you get back a nice JSON blob.  the more difficult (and i anticipate less-stable) version gives a JS bundle that you can parse the solutions from.
- old solutions are saved in a database.  is this necessary?  no.  would it be useful one day?  also probably not, but you never know.
- we try to be responsible!  we check the db for today's solution before making a request to the nyt's servers.  if today's solution isn't up yet, we give the latest solution that *is* up, and we show that (old) solution until at least an hour is elapsed and we make another request.
- alas, there's no support for the crossword, as it's behind a paywall.

view the final product at https://nyt.wtf
