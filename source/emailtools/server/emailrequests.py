import emailtools.server.reader as reader
import emailtools.server.sender as sender
import asyncio
import inspect

# Global list to keep track of all route handlers
route_handlers = []


def route(email, password, page, toret):
    def decorator(func):
        # Store the route configuration and function
        route_config = {
            'email': email,
            'password': password,
            'page': page,
            'toret': toret,
            'func': func
        }
        route_handlers.append(route_config)
        return func

    return decorator


async def run_email_handler(handler):
    """Run individual email handler in background"""
    while True:
        try:
            request = reader.Reader(
                f"imap.{handler['email'].split('@')[1]}",
                handler['email'],
                handler['password']
            )

            # Add safety checks to prevent index errors
            if (request.answers and
                    len(request.answers) > 0 and
                    len(request.answers[0].split(' ')) > 1):

                page_from_request = request.answers[0].split(' ')[1]

                if page_from_request == handler['page']:
                    sender.Sender(
                        f"imap.{handler['email'].split('@')[1]}",
                        handler['email'],
                        handler['password'],
                        request.from_addr,
                        {
                            'number': handler['toret'][0],
                            'name': handler['toret'][1],
                            'html': handler['func']()
                        }
                    )
            else:
                print(f"No valid answers found in request: {request.answers}")

            await asyncio.sleep(1)  # Check every second
        except Exception as e:
            print(f"Error in email handler: {e}")
            await asyncio.sleep(5)  # Wait before retrying


async def start_all_handlers():
    """Start all registered route handlers"""
    tasks = []
    for handler in route_handlers:
        task = asyncio.create_task(run_email_handler(handler))
        tasks.append(task)

    # Wait for all tasks to complete (they run forever)
    await asyncio.gather(*tasks)
