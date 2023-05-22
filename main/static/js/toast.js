let reportToastTrigger = document.querySelectorAll(".report-toast-trigger");
const toastLiveExample = document.getElementById('liveToast')

if (reportToastTrigger) {
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
    reportToastTrigger.forEach((element) => {
        element.addEventListener('click', () => {
            toastBootstrap.show()
        })
    }
    )
}