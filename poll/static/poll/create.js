var current_option = 0

function addOption() {
    var element = document.getElementById('add-option')
    var html = `
    <div class="row mt-4" id="current-option-${current_option}">
        <div class="form-group col-md-5">
            <label >Option </label>
            <input type="text" required class="form-control"  name="options" placeholder="enter text">
        </div>

        <div class="form-group col-md-3 ">
            <button type="button" onclick="removeOption(${current_option})" class="btn btn-danger mt-4" >Remove</button>
        </div>
    </div>
    `

    element.innerHTML += html
    current_option += 1


}

function removeOption(id) {
    var element = document.getElementById(`current-option-${id}`)
    element.remove()

}