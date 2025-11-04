# 🧩 Microservices Orchestration Demo (FastAPI + Async Python)

This project demonstrates how to **orchestrate multiple microservices** using Python’s **FastAPI** and **httpx** (for async API calls).  
It shows how an *orchestrator service* coordinates three independent microservices — **User**, **Product**, and **Payment** — to complete a single workflow: **placing an order**.

---

## 🚀 Overview

### Problem
In a microservice architecture, different services own different parts of the data:
- **User Service** → user profiles and membership
- **Product Service** → product catalog, stock, and pricing
- **Payment Service** → payment and transaction processing

When a user places an order, the system needs to:
1. Fetch user details  
2. Fetch product details  
3. Process payment  
4. Combine everything into one final response

This coordination process is called **Orchestration**.

---

## 🧠 What is Orchestration?

> Orchestration means a central service controls and coordinates multiple microservices to complete a business workflow.

It’s like a **conductor in an orchestra**: each musician (microservice) plays their part, and the conductor (orchestrator) ensures it all happens in sync.

---

## ⚙️ Project Structure

