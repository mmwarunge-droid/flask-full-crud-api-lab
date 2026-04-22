from flask import Flask, jsonify, request


'''
This API:

Allows users to add a new event with a POST request to /events.
Lets users update an existing event title via PATCH to /events/<id>.
Enables users to remove an event by sending a DELETE to /events/<id>.
The API should respond with structured JSON and appropriate HTTP status codes
'''
app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json() or {}
    title = data.get("title")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    new_id = max((event.id for event in events), default=0) + 1
    new_event = Event(new_id, title)
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json() or {}
    title = data.get("title")

    for event in events:
        if event.id == event_id:
            if title:
                event.title = title
            return jsonify(event.to_dict()), 200

    return jsonify({"error": "Event not found"}), 404


# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    for i, event in enumerate(events):
        if event.id == event_id:
            del events[i]
            return "", 204

    return jsonify({"error": "Event not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)