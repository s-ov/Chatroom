# 💬 Chatroom — Flask Application with Authentication and Social Features

**Chatroom** is a Flask-based social app built with the **application factory pattern**. 
It supports user authentication, profile interactions (follow/unfollow), post creation, 
and a workflow for rendering user-focused content.

The project is modular, testable, and emphasizes **separation of concerns** across three core apps: 
`auth`, `posts`, and `workflow`.


## 🧩 Project Structure
---

## 🔐 `auth` App
Manages user authentication and profile management.

### Blueprints:
- **`auth_bp`**:
  - User registration and login
  - Password reset functionality using [`flask-mailman`]
  - Sends password reset URL to user's email using `EmailMessage`

- **`user_bp`**:
  - Fetch user profile
  - Edit and delete profile
  - Follow and unfollow other users

### Models:
- `User`
- `followers` (many-to-many self-referencing association table):


## 🔐 `posts` App
Manages posts manipulations logic.

### Blueprints:
- **`posts_bp`**:
  - Create new posts
  - Delete existing posts (with appropriate authorization)


## 🔁 `workflow` App
Provides loosely coupled rendering of profile and chatroom pages using logic 
that integrates data from auth and posts.

### Blueprints:
- **`workflow_bp`**:
  - Renders user profiles (with their posts)
  - Renders chatroom page (includes posts from followed users and with their posts)


## 🛠️ Tech Stack
    - Flask
    - Flask-Mailman
    - SQLAlchemy
    - Jinja2
    - Bootstrap (via templates)
    - pytest (partial test coverage)


## ✅ Testing

Project includes partial test coverage for:
- Authentication
- Profile routes
- Post creation logic

Testing is designed with future expansion in mind.
