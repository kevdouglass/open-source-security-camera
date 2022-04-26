from django.shortcuts import render, redirect
from userconfig.forms import CameraEntryForm, CameraViewForm, StorageForm


def settings(request):
    # this_user = User.objects.get(username=request.user.username)
    from userconfig.models import Camera
    from userconfig.models import CameraView
    from userconfig.models import Storage
    # if there are no cameras create a dummy camera
    if (Camera.objects.count() < 1):
        Camera.objects.create(
            deviceName='rpi camera 01',
        )
    # if there are no views create a dummy view
    if (CameraView.objects.count() < 1):
        CameraView.objects.create(
            showMotionBoxes='True',
            showText='True',
            text='Cam Name :: Date :: Time',
            fps='30',
            invert='False',
            mirror='False',
            scale='0.75'
        )
    # if there are no storages create a dummy storage
    if (Storage.objects.count() < 1):
        Storage.objects.create(
            recordToDevice='False',
            filePath='/home/pi/open-source-security-camera/osCam/videos/',
            maxSpace='100',
            timeToLive='60',
            lengthOfRecordings='10',
        )
    pageData = {
        'cameras': Camera.objects.all(),
        'views': CameraView.objects.all(),
        'storages': Storage.objects.all(),
        }
    # save camera settings
    if(request.method == 'POST'):
        if("add_camera_config" in request.POST):
            add_form = CameraEntryForm(request.POST)
            # check that form is valid
            if(add_form.is_valid()):
                deviceName = add_form.cleaned_data['deviceName']
                thisCamInstance = Camera.objects.get(id=1)
                thisCamInstance.deviceName = deviceName
                thisCamInstance.save()
            return redirect('/settings')
        # save view settings
        elif("add_view_config" in request.POST):
            addForm = CameraViewForm(request.POST)
            if(add_form.is_valid()):
                showMotionBoxes = addForm.cleaned_data['showMotionBoxes']
                showText = addForm.cleaned_data['showText']
                text = addForm.cleaned_data['text']
                fps = addForm.cleaned_data['fps']
                invert = addForm.cleaned_data['invert']
                mirror = addForm.cleaned_data['mirror']
                scale = addForm.cleaned_data['scale']
                # update this instance
                thisViewInstance = CameraView.objects.get(id=1)
                thisViewInstance.showMotionBoxes = showMotionBoxes
                thisViewInstance.showText = showText
                thisViewInstance.text = text
                thisViewInstance.fps = fps
                thisViewInstance.invert = invert
                thisViewInstance.mirror = mirror
                thisViewInstance.scale = scale
                thisViewInstance.save()
            return redirect('/settings')
        # add storage settings
        elif ("add_storage_config" in request.POST):
            addForm = StorageForm(request.POST)
            # check submision form valididity
            if(add_form.is_valid()):
                recordToDevice = addForm.cleaned_data['recordToDevice']
                filePath = addForm.cleaned_data['filePath']
                maxSpace = addForm.cleaned_data['maxSpace']
                timeToLive = addForm.cleaned_data['timeToLive']
                lengthOfRecordings = addForm.cleaned_data['lengthOfRecordings']
                thisStorageInstance = Storage.objects.get(id=1)
                thisStorageInstance.recordToDevice = recordToDevice
                thisStorageInstance.filePath = filePath
                thisStorageInstance.maxSpace = maxSpace
                thisStorageInstance.timeToLive = timeToLive
                thisStorageInstance.lengthOfRecordings = lengthOfRecordings
                thisStorageInstance.save()
                return redirect('/settings')
    elif(request.method == "GET"):
        Camera = Camera.objects.get(id=1)
        cameraFormData = CameraEntryForm(
            initial={
                'deviceName': Camera.deviceName,
            }
        )
        Camera = cameraFormData.save(commit=False)
        CameraView = CameraView.objects.get(id=1)
        viewForm = CameraViewForm(
            instance=CameraView,
            initial={
                'showMotionBoxes': CameraView.showMotionBoxes,
                'showText': CameraView.showText,
                'text': CameraView.text,
                'fps': CameraView.fps,
                'invert': CameraView.invert,
                'mirror': CameraView.mirror,
                'scale': CameraView.scale,
                }
        )
        CameraView = viewForm.save(commit=False)
        Storage = Storage.objects.get(id=1)
        storageFormData = StorageForm(
            instance=Storage,
            initial={
                'recordToDevice': Storage.recordToDevice,
                'filePath': Storage.filePath,
                'maxSpace': Storage.maxSpace,
                'timeToLive': Storage.timeToLive,
                'lengthOfRecordings': Storage.lengthOfRecordings,
            }
        )
        Storage = storageFormData.save(commit=False)
        pageData = {
            "camera_form_data": cameraFormData,
            "view_form_data": viewForm,
            "storage_form_data": storageFormData,
        }
    return render(request, 'user/settings.html', pageData)
