document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.alert').forEach((el) => {
    setTimeout(() => {
      if (el.classList.contains('alert-success') || el.classList.contains('alert-info')) el.remove();
    }, 5000);
  });
});
