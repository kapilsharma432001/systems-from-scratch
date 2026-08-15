# Event-Driven Architecture

![A simple event driven architecture](image-11.png)

- The entire system is not event-driven. The producer is **schedule-driven** because EventBridge Scheduler invokes the worker every 15 minutes.
- From SQS to the Notifo Lambda function, the pipeline becomes event-driven.
- Describing it as a **scheduled producer feeding an event-driven pipeline** is technically more accurate.
- The main reasons for using SQS with two Lambda functions are decoupling, buffering, independent scaling, and failure isolation.

## Why Do We Use a Queue at All?

Forget AWS for a moment. Whether the underlying technology is SQS, RabbitMQ, or Kafka, the basic purpose is the same:

- A queue sits between a producer and a consumer so that they don't have to process work at the same time or at the same speed.

In our case:

```text
Worker Lambda (producer) -> SQS -> Notifo Lambda (consumer)
```

Without a queue:

```text
Worker Lambda -> Notifo Lambda
```

The two Lambda functions are directly dependent on each other.

With a queue:

```text
Worker Lambda -> SQS -> Notifo Lambda
```

The two Lambda functions are now decoupled.

### Main Benefits of Using a Queue

1. **Decoupling:** Worker Lambda does not need to know whether Notifo Lambda is available at that moment.
2. **Buffering:** Suppose Worker Lambda suddenly creates 20,000 notification events.

   ```text
   20,000 events -> SQS -> Notifo Lambda processes them at its own rate
   ```

   SQS absorbs the spike.

3. **Independent Scaling:** As the queue backlog grows, AWS can run more Notifo Lambda invocations without scaling Worker Lambda.
4. **Retries:** Failed messages can be retried automatically.
5. **Backpressure:** If downstream processing is slower than incoming traffic, the queue holds the backlog instead of overwhelming the service.
