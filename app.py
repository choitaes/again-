from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.2kwqhph.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

@app.route('/')
def home():
	return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
	url_receive = request.form['url_give']
	comment_receive = request.form['comment_give']
	star_receive = request.form['star_give']
	
	headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
	data = requests.get(url_receive,headers=headers) #url_receive에 있는 url 주소에서 정보를 가져온다
	soup = BeautifulSoup(data.text, 'html.parser')

	#메타데이터 가져오기
	ogtitle = soup.select_one('meta[property="og:title"]')['content']
	ogdesc = soup.select_one('meta[property="og:description"]')['content']
	ogimage = soup.select_one('meta[property="og:image"]')['content']

	#DB에 데이터 저장
	
	doc = { 
		'title':ogtitle,
		'desc':ogdesc,
		'image':ogimage,
		'comment':comment_receive,
		'star':star_receive
	}
	
	db.movies.insert_one(doc)

	return jsonify({'msg':'저장완료!'})

@app.route("/movie", methods=["GET"])
def movie_get():
	all_movies = list(db.movies.find({},{'_id':False}))

	return jsonify({'result':all_movies})

if __name__ == '__main__':
	app.run('0.0.0.0', port=5000, debug=True)
	


"""
이부분 추가했다
"""