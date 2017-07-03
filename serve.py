import cvfy
import predict
import hashlib

app = cvfy.register("nongh:0.0.0.0:5431785:5001:8000:0.0.0.0")

img_dict = {}

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

@cvfy.crossdomain
@app.listen()
def runner():
    all_image_paths = cvfy.getImageArray()
    err_list = []
    
    if not all_image_paths:
	    err_list.append("Please upload an image first")
	
    cvfy.sendTextArray(err_list)
	return 'OK'
    
    all_text = cvfy.getTextArray()

    if not all_text:
	    err_list.append("Please add a question first")
	
    cvfy.sendTextArray(err_list)
	return 'OK'
		
    question = ' '.join(all_text)
    img_fname = all_image_paths[0]
    checksum = md5(img_fname)
    if img_dict.has_key(checksum):
        img_features = img_dict[checksum]
        answer = predict.serve(img_features, question)
    else:
        img_features = predict.calcFeatures(img_fname)
        img_dict[checksum] = img_features
        answer = predict.serve(img_features, question)
    
    cvfy.sendTextArray(answer)
    return 'OK'

app.run()
