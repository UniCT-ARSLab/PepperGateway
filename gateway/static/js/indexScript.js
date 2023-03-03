function showItem(id) {
    const item = document.getElementById(id);
    item.classList.toggle("hidden");
}
function hideItem(id) {
    const item = document.getElementById(id);
    item.classList.add("hidden");
}