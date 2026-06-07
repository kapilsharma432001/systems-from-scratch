## Common Patterns
#### Recognize -> apply -> explain tradeoff

- Just remember, **patterns are often combined, not used independently, and recognizing them helps you avoid reinventing the wheel during interviews.**

#### The main patterns to know:

| Pattern                    | When you should recognize it           | Common examples                                     |
| -------------------------- | -------------------------------------- | --------------------------------------------------- |
| **Real-time updates**      | “Users should see updates instantly”   | Chat, notifications, live comments, live dashboards |
| **Long-running tasks**     | “This operation takes seconds/minutes” | Video encoding, report generation, file processing  |
| **Contention handling**    | “Many users compete for same resource” | Last ticket, inventory, auction bidding             |
| **Scaling reads**          | “Too many users are reading data”      | Feeds, product pages, profiles, posts               |
| **Scaling writes**         | “Too many writes are hitting one DB”   | Logs, metrics, likes, chat messages                 |
| **Large blob handling**    | “Users upload/download large files”    | Videos, images, PDFs, backups                       |
| **Multi-step processes**   | “Business flow has many steps”         | Checkout, payment, order fulfillment, onboarding    |
| **Proximity-based search** | “Find nearby things”                   | Uber drivers, nearby restaurants, delivery partners |

##### 1. Real-time Updates
- Use this when the interviewer says:
    - chat messages should appear instantly
    - live comments
    - driver location should update
    - notification should appear immediately

- Basic options: Polling -> SSE -> WebSockets
- **Start simple with polling. Use WebSockets/SSE when low-latency updates are truly required.**

###### Polling vs SSE vs WebSockets

Core difference: **polling means the client keeps asking**, **SSE means the server pushes updates to the client**, and **WebSockets means both client and server can send messages anytime**.

| Approach | How it works | Best for | Main tradeoff |
| -------- | ------------ | -------- | ------------- |
| **Polling** | Client repeatedly asks the server for updates every few seconds. | Simple updates, low-scale systems, cases where slight delay is acceptable. | Easy to build, but can waste requests when nothing changed. |
| **SSE** | Client opens one long-lived HTTP connection, and the server pushes updates to the client. | One-way real-time updates like notifications, live feeds, progress updates, dashboards. | Simpler than WebSockets, but only server-to-client. |
| **WebSockets** | Client and server keep a persistent two-way connection open. | Chat, multiplayer games, collaborative editing, live bidirectional communication. | Powerful, but more operationally complex. |

###### Polling

- The client sends a request like "Any new updates?" every fixed interval, for example every 5 seconds.
- This is the simplest option because it uses normal HTTP requests.
- It works well when updates are not very frequent or real-time accuracy is not strict.
- The downside is wasted work: if there are no updates, the server still receives repeated requests.
- Polling also adds delay because the user only sees the update on the next poll.

###### SSE

- SSE stands for Server-Sent Events.
- The client makes one HTTP request and keeps the connection open.
- Whenever the server has new data, it sends an event on that same connection.
- It is a good fit when updates only need to flow from server to client.
- Compared to polling, SSE avoids repeated empty requests and usually feels more real time.
- Compared to WebSockets, SSE is simpler because it still works over HTTP and is only one-way.

> 💡 **Interview insight**
>
> In interviews, quickly recognize the pattern from the requirement, apply the simplest correct architecture, then discuss tradeoffs. For real-time updates, use polling for simple low-scale cases, SSE for one-way updates, and WebSockets for bidirectional real-time communication.

#### 2. Long-running tasks
- Use this when something can not finish inside a normal API request.
- For example:-
    - User uplaods video -> video needs transcoding
- Bad design:-
    - POST /upload waits 5 minutes until transcoding completes

- Better design:-
    - API server stores request
    - Pushes jobs to queue
    - Returns job_id immediately
    - Worker picks up the job
    - User checks status later

- Simple architecture:-
    - Client -> API Server -> Queue -> Worker -> DB

> 💡 **Interview insight**
>
> If the task takes more than a few seconds, use async processing with a queue and worker pool.

- Examples: Video transcoding, PDF generation, Bulk email sending, Data export, ML processing etc.

#### 3. Contention Handling
- Use this when multiple users modify the same resource.
- Example:-
    - Only 1 concert ticket left.
    - 100 users click “Buy” at the same time.

- Problem: Without protection, you may sell the same ticket twice.
- Common Solutions:-
    