# 🚀 Real-Time Cloud-Based Event Planning & RSVP Tracker

![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)
![License](https://img.shields.io/badge/License-MIT-green)

A cloud-native, real-time event planning and RSVP tracking platform featuring token-based frictionless guest responses, automated concurrency-safe capacity enforcement, waitlists, and live Server-Sent Events (SSE) dashboard metrics.

---

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Problem Statement](#-problem-statement)
- [System Objectives](#-system-objectives)
- [Industry Relevance](#-industry-relevance)
- [Cloud Computing Concepts Demonstrated](#-cloud-computing-concepts-demonstrated)
- [Key Features](#-key-features)
- [Folder Structure](#-folder-structure)
- [Installation & Setup Guide](#-installation--setup-guide)
- [How to Run the Application](#-how-to-run-the-application)
- [Concurrency & Race Condition Handling](#-concurrency--race-condition-handling)
- [Author & License](#-author--license)

---

## 📌 Project Overview
Managing events via static spreadsheets or messaging groups leads to duplicate submissions, untracked plus-ones, and inaccurate headcounts. This system models a modern event management architecture where organizers publish events, generate unique secure tokens, and monitor live attendee counts across connected client dashboards in real time.

## ⚠️ Problem Statement
* **Data Discrepancies:** Manual lists fail to handle simultaneous updates or last-minute cancellations accurately.
* **Overbooking Risks:** Multiple attendees trying to claim the final available seat can breach venue capacity limits without atomic database locking.
* **Refresh Latency:** Organizers lack instant visibility into live attendance numbers without manual dashboard reloads.

## 🎯 System Objectives
1. **Frictionless Guest RSVPs:** Allow attendees to respond securely via unique tokens (`tok_abc123`) without mandatory user registration[cite: 1].
2. **Real-Time Synchronization:** Push live counter updates (`Going`, `Maybe`, `Not Going`, `Waitlist`) across active dashboards using Server-Sent Events[cite: 1, 2].
3. **Safe Capacity Enforcement:** Automatically intercept over-capacity requests and route excess attendees to a managed waitlist queue[cite: 1, 2].

## 🏭 Industry Relevance
* **Corporate & Academic Conferences:** Streamlining guest check-ins and capacity capping for workshops and seminars.
* **Ticketing & Event Tech:** Mirrors core operational logic utilized by commercial platforms like Eventbrite and Cvent.
* **Operational Efficiency:** Reduces no-shows and eliminates administrative coordination overhead.

---

## ☁️ Cloud Computing Concepts Demonstrated
* **Client-Server Architecture:** Decoupled REST API backend communicating asynchronously with interactive HTML/JS frontends[cite: 1, 2].
* **Real-Time Push Communication:** Utilizing Server-Sent Events (SSE) for low-latency state broadcasting.
* **Atomic Transactions & Concurrency Control:** Enforcing strict conditional database updates to prevent race conditions during high-traffic seat reservations[cite: 1, 2].
* **Environment Configuration:** Secure separation of runtime parameters using configuration templates.

---

## ✨ Key Features
* **Event Management Module:** Create and manage events with customizable titles, venues, dates, and strict seating capacities[cite: 1, 2].
* **Token-Based Invite System:** Secure invitation mapping that prevents duplicate entries per user per event[cite: 1, 2].
* **Automated Waitlist Engine:** Automatically shifts respondents to a waitlist status once maximum capacity is reached[cite: 1, 2].
* **Live SSE Analytics Dashboard:** Instant visualization of seat utilization percentages and response distributions[cite: 1, 2].

---

## 📂 Folder Structure
```text
Real-Time-Cloud-Event-RSVP-Tracker/
│
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment configuration template
├── main.py                        # FastAPI backend, SQLite database, & SSE engine[cite: 1, 2]
├── templates/
│   └── index.html                 # Interactive Organizer & Attendee Dashboard[cite: 1, 2]
└── README.md                      # Project documentation
