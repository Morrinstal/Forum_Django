document.addEventListener("DOMContentLoaded", () => {
    const likeForms = document.querySelectorAll(".like-form");

    likeForms.forEach((form) => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const button = form.querySelector(".like-btn");
            const likeCountElement = form.nextElementSibling; 
            const formData = new FormData(form);
            const url = form.action;

            try {
                const response = await fetch(url, {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest", 
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    const { like_count, liked, post_id } = data;

                    likeCountElement.textContent = like_count;

                    if (liked) {
                        button.classList.add("btn-primary");
                        button.classList.remove("btn-outline-secondary");
                    } else {
                        button.classList.add("btn-outline-secondary");
                        button.classList.remove("btn-primary");
                    }

                    const relatedLikeElement = document.querySelector(`#like-count-${post_id}`);
                    if (relatedLikeElement) {
                        relatedLikeElement.textContent = like_count;
                    }
                } else {
                    console.error("Ошибка при обработке лайка:", response.status);
                }
            } catch (error) {
                console.error("Ошибка при выполнении запроса:", error);
            }
        });
    });
});
