async function handleRouteChange() {
    const path = window.location.pathname;
    const contentElement = document.getElementById('content');
  
    contentElement.innerHTML = '';
  
    if (path === '/') {
      contentElement.innerHTML = '<h1>Welcome to My Blog</h1>';
    } else if (path === '/blog') {
      try {
        const response = await fetch('/blog-posts');
        const blogPosts = await response.json();
  
        blogPosts.forEach((post) => {
          const blogPostElement = document.createElement('div');
          blogPostElement.classList.add('blog-post');
  
          const titleElement = document.createElement('h2');
          titleElement.textContent = post.title;
  
          const authorElement = document.createElement('p');
          authorElement.textContent = `Written by ${post.author}`;
  
          const contentElement = document.createElement('div');
          post.content.forEach((paragraph) => {
            const paragraphElement = document.createElement('p');
            paragraphElement.textContent = paragraph;
            contentElement.appendChild(paragraphElement);
          });
  
          blogPostElement.appendChild(titleElement);
          blogPostElement.appendChild(authorElement);
          blogPostElement.appendChild(contentElement);
  
          contentElement.appendChild(blogPostElement);
        });
      } catch (error) {
        console.error('Failed to fetch blog post data:', error);
      }
    } else {
      contentElement.innerHTML = '<h1>Page Not Found</h1>';
    }
  }
  
  window.addEventListener('popstate', handleRouteChange);
  
  handleRouteChange();
  