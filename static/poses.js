// Define an array of pose names and image URLs
const poses = [
    { name: "anantasana", image: "static\\images\\anantasana.png" },
    { name: "ardha uttanasana", image: "static\\images\\ardha uttanasana.png" },
    { name: "bhujangasana", image: "static\\images\\bhujangasana.png" },
    { name: "chakravakasana", image: "static\\images\\chakravakasana.png" },
    { name: "dandasana", image: "static\\images\\dandasana.png" },
    { name: "makarasana", image: "static\\images\\makarasana.png" },
    { name: "sukhasana", image: "static\\images\\sukhasana.png" },
    { name: "urdhva mukha svanasana", image: "static\\images\\urdhva mukha svanasana.png" },
    { name: "utkatasana", image: "static\\images\\utkatasana.jpg" },
    { name: "uttana shishosana", image: "static\\images\\uttana shishosana.png" },
    { name: "utthita trikonasana", image: "static\\images\\utthita trikonasana.png" },
    { name: "vajrasana", image: "static\\images\\vajrasana.png" },
    { name: "virbhadrasana", image: "static\\images\\virbhadrasana.png" },
    { name: "vriksasana", image: "static\\images\\vriksasana.png" },
    { name: "vrischikasana", image: "static\\images\\vrischikasana.png" },
    { name: "malasana", image: "static\\images\\malasana.png" }
];

// Function to populate the select dropdown with pose names
function populateSelect() {
    const select = document.getElementById('pose-select');
    poses.forEach((pose, index) => {
        const option = document.createElement('option');
        option.value = index;
        option.textContent = pose.name;
        select.appendChild(option);
    });
}

// Function to display the selected pose
function displaySelectedPose() {
    const selectedIndex = document.getElementById('pose-select').value;
    const pose = poses[selectedIndex];
    const poseContainer = document.getElementById('pose-container');

    if (selectedIndex !== '') {
        document.getElementById('pose-name').textContent = pose.name;
        document.getElementById('pose-image').src = pose.image;
        poseContainer.classList.remove('hidden'); // Show the pose container
    } else {
        poseContainer.classList.add('hidden'); // Hide the pose container
    }
}

// Populate the select dropdown when the page loads
populateSelect();
