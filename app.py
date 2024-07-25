from flask import Flask, render_template, request, redirect, url_for
import json 


app = Flask(__name__)

def get_storage():
    try:
        with open("storage.json", "r") as handler:
            storage_list = json.load(handler)
    except (FileNotFoundError, json.JSONDecodeError):
        storage_list = []
    return storage_list

def save_storage(data):
    with open("storage.json", "w") as handler:
        json.dump(data, handler, indent=1)

def add_storage(data):
    storage_list = get_storage()
    storage_list.append(data)
    save_storage(storage_list)

def fetch_post_by_id(post_id):
    storage = get_storage()
    fetched_post = [post for post in storage if post["id"] == post_id]
    if len(fetched_post) == 0:
        return None
    return fetched_post[0]


@app.route('/')
def index():
    return render_template("index.html", storage=get_storage())


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        storage = get_storage()
        if len(storage) != 0:
            id = get_storage()[-1]["id"] + 1
        else:
            id = 0 
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")
        add_storage({"id": id, "author": author, "title": title, "content": content})
        return redirect(url_for("index"))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Find the blog post with the given id and remove it from the list
    # Redirect back to the home page
    storage = get_storage()
    new_storage = [post for post in storage if post["id"] != post_id]
    save_storage(new_storage)
    return redirect(url_for("index"))
    
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    print(post)
    if post is None:
        # Post not found
        return "Post not found", 404
    
    if request.method == 'POST':
        # Update the post in the JSON file
        # Redirect back to index
        id = post_id
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")
        updated_post = {"id": id, "author": author, "title": title, "content": content}
        storage = get_storage()
        deleted_post = [post for post in storage if post["id"] != post_id]
        updated_storage = deleted_post.append(updated_post)
        save_storage(updated_storage)
        return redirect(url_for("index"))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)    



if __name__ == '__main__':
    app.run()