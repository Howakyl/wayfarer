const confirmDelete = document.querySelector('.confirm-delete');
const deleteForm = document.querySelector('.delete-form')
const selectEl1 = document.getElementById('id_user');
const selectEl2 = document.getElementById('id_city');
  
M.FormSelect.init(id_user)
M.FormSelect.init(id_city)

confirmDelete.addEventListener('click' ,  () => {
    const input =  prompt('Are you sure you want to delete this post?');
    if (input === 'yes') {
        deleteForm.classList.toggle('hidden');
        confirmDelete.classList.toggle('hidden');
    } else {
        return alert('You did not delete your post');
    }
});