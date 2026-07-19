 ## Designing Rate Limiter
 #### What is rate limiter?

 - A rate limiter controls how many requets a client can make within a specific timeframe. 
 - It acts like a traffic controller for your API - allowing for example "100 requests per minute" from a user, then rejecting excess requests with an HTTP 429 "Too Many Requests" response.
 - Prevents abuse, protects your servers from being overwhelmed by bursts of traffic, and ensure fair usage across all users.


 