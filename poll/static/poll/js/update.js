var current_option = 0

const addImageNow = document.getElementById('image-body')
if(addImageNow) {
    addImageNow.addEventListener('click', addImage, false);
}

function addImage() {
    var element = document.getElementById('add-option')
    var html = `
    <div class="row mt-4" id="current-option-${current_option}">
        <div class="form-group col-md-5">
            <label >Image </label>
            <input style="height: 26px; padding:0px" type="file" required class="form-control"  name="images" accept="image/*">
        </div>

        <div class="form-group col-md-3 ">
            <button type="button" style="width:188px;height:50px;" onclick="removeOption(${current_option})" class="lgn-btn btn-danger">Remove
                <i class="fa fa-trash"></i>
            </button>
        </div>
    </div>
    `

    element.innerHTML += html
    current_option += 1


}

function addOption() {
    var element = document.getElementById('add-option')
    var html = `
    <div class="row mt-4" id="current-option-${current_option}">
        <div class="form-group col-md-5">
            <label >Option </label>
            <input type="text" required class="form-control"  name="options" placeholder="enter text">
        </div>

        <div class="form-group col-md-3 ">
            <button type="button" style="width:188px;height:50px;" onclick="removeOption(${current_option})" class="lgn-btn btn-danger">Remove
            <i class="fa fa-trash"></i>
            </button>
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