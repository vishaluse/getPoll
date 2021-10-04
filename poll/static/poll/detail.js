console.log("hehe boi")

const optionBox = document.getElementById('option-box')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
const timerBox = document.getElementById('timer-box')



const url = window.location.href

const activateTimer = (time) => {
    if (time.toString().length < 2) {
        timerBox.innerHTML = `<b>0${time}:00</b>`
    } else {
        timerBox.innerHTML = `<b>${time}:00</b>`
    }

    let minutes = time - 1
    let seconds = 60
    let displaySeconds
    let displayMinutes

    const timer = setInterval(()=>{
        seconds --
        if (seconds < 0) {
            seconds = 59
            minutes --
        }
        if (minutes.toString().length < 2) {
            displayMinutes = '0'+minutes
        } else {
            displayMinutes = minutes
        }
        if(seconds.toString().length < 2) {
            displaySeconds = '0' + seconds
        } else {
            displaySeconds = seconds
        }
        if (minutes === 0 && seconds === 0) {
            timerBox.innerHTML = "<b>00:00</b>"
            setTimeout(()=>{
                clearInterval(timer)
                alert('Time over')
                sendData()
            }, 500)
        }

        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`
    }, 1000)
}


// const activateTimer = (time) => {

//     if(localStorage.getItem("count_timer")){
//         var count_timer = localStorage.getItem("count_timer");
//     } else {
//         var count_timer = time*60;
//     }
//     var minutes = parseInt(count_timer/60);
//     var seconds = parseInt(count_timer%60);
//     function countDownTimer(){
//         if(seconds < 10){
//             seconds= "0"+ seconds ;
//         }if(minutes < 10){
//             minutes= "0"+ minutes ;
//         }
        
//         document.getElementById("timer-box").innerHTML = "Time Left : "+minutes+" Minutes "+seconds+" Seconds";
//         if(count_timer <= 0){
//             localStorage.clear("count_timer");
//         } else {
//             count_timer = count_timer -1 ;
//             minutes = parseInt(count_timer/60);
//             seconds = parseInt(count_timer%60);
//             localStorage.setItem("count_timer",count_timer);
//             setTimeout("countDownTimer",1000);
//         }
//     }
//     setTimeout("countDownTimer()",1000);
// }



$.ajax({
    type: 'GET',
    url: `${url}/data`,
    success: function(response){
        console.log(response)
        const data = response.data
        for (const [key, value] of Object.entries(data)) {
            optionBox.innerHTML += `
                    <hr>
                    <div  class="mb-2">
                        <b>${key}</b>
                    </div>
                `
                value.forEach(v=>{
                    optionBox.innerHTML += `
                        <div>
                            <input type="radio" class="ans" id="${key}-${v}" name="${key}" value="${v}">
                            <label for="${key}">${v}</label>
                        </div>
                    `
                })
          }
          activateTimer(response.time)
    },
    error: function(error){
        console.log(error)
    }
})

const optionForm = document.getElementById('option-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')



const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    // console.log(elements)
    data['csrfmiddlewaretoken'] = csrf[0].value
   
    // console.log(data)
    elements.forEach(el=>{
        if(el.checked) {
            data[el.name] = el.value
        } else {
            if(!data[el.name]) {
                data[el.name] = null
            }
        }
    })


    $.ajax({
        type: 'POST',
        url: `${url}/save`,
        data: data,
        success: function(response){
            console.log(response)
        },
        error: function(error){
            console.log(error)
        }
    })
}

optionForm.addEventListener('submit', e=>{
    e.preventDefault()
    sendData()
})