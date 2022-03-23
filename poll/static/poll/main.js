console.log('hello world')

const modalBtns = [...document.getElementsByClassName('modal-button')]

const startBtn = document.getElementById('start-button')

const url = window.location.href

modalBtns.forEach(modalBtn=> modalBtn.addEventListener('click', ()=>{
    console.log(modalBtn)
   
    const pk = modalBtn.getAttribute('data-pk')
    console.log(pk)
   
    startBtn.addEventListener('click',()=>{
        window.location.href = url + pk
    })

}))