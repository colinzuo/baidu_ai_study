# baidu_ai_study

1. Add user face image

	https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add
	
2. Search user face image

	https://aip.baidubce.com/rest/2.0/face/v3/search
	
3. Test

	Add star face image from baidu, 9 stars each with 4 face images
	
	verify with star face image from google, same 9 stars each with 4 face images
	
	Result:
	
		28 are correct and with score higher than 80
		7 are correct but with score between 60 and 80
		1 is wrong with score 34.97

	Cost:
	
		free, but with a constraint of 2 api calls per second mostly