# ITNE352-Project---Sec-1---Group-A10

# ITNE352 Recipe Discovery System

## Project Description

This project is a client-server recipe discovery system developed using Python sockets and TheMealDB API.

The system allows users to:

* Search recipes by name
* Filter recipes by category
* Filter recipes by area
* Filter recipes by ingredient
* View random recipes
* Browse reference lists

The server handles API communication and multiple client connections, while the client provides a user-friendly interface for interacting with the system.

---

## Semester

Semester 2, 2025-2026

---

## Group Information

Course: ITNE352 Network Programming

Group Members:

Zainab Taha Mohammed Al-Naham 202305105 @ZIXP01
        @rawanread

---

## Requirements

Install Python 3.

Required libraries:

* socket
* json
* requests
* threading

Install requests library:

```bash
pip install requests
```

---

## How to Run

### Start the server

```bash
python server.py
```

### Start the client

```bash
python client.py
```

---

## Project Files

### Client Files

* client.py → Main client program
* menus.py → Client menus
* display.py → Display functions

### Server Files

* server.py → Main server program
* api_handler.py → API requests
* cache.py → Reference cache handling

---

## Features

* TCP socket communication
* Multi-client support using threads
* JSON message exchange
* API integration
* Reference cache
* Recipe search and filtering

---

## Conclusion

This project demonstrates the implementation of a client-server architecture using Python sockets, APIs, JSON, and multithreading.

---

## Acknowledgments

* University of Bahrain
* TheMealDB API
