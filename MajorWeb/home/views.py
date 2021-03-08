from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.

import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

onBasisPost = []
onBasisVideos = []
onBasisCosine = []
onBasisAll = []

onBasisPostLinks = []
onBasisVideosLinks = []
onBasisCosineLinks = []
onBasisAllLinks = []


def redu(cate, countr):
    data = pd.read_csv(
        'C:\\Users\\shash\\Desktop\\Data_Science\\Major2020\\webScrapping/final_dataset.csv', encoding='unicode_escape')
    if(countr != 'empty'):
        indexes = data[data['country'] != countr].index
        data.drop(indexes, inplace=True)
    if(cate != 'empty'):
        indexes = data[data['category'] != cate].index
        data.drop(indexes, inplace=True)
    return data


def cosineSimilairty(cate, countr, productDescription, hashtags):
    data = redu(cate, countr)
    data = data[['name', 'description', 'tagged_names']]
    df = []
    df.insert(0, {'name': 'aaa', 'description': productDescription,
                  'tagged_names': hashtags})
    data = pd.concat([pd.DataFrame(df), data], ignore_index=True)
    indices = pd.Series(data.name)
    data.set_index('name', inplace=True)
    index = 0
    data['bag_of_words'] = ''
    columns = data.columns
    for index, row in data.iterrows():
        words = ""
        for col in columns:
            words = words + ' '+row[col]
        row['bag_of_words'] = words
    data.drop(columns=[col for col in data.columns if col !=
                       'bag_of_words'], inplace=True)
    count = CountVectorizer()
    count_matrix = count.fit_transform(data['bag_of_words'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    idx = 0
    score_series = pd.Series(cosine_sim[idx])
    data = data.drop('bag_of_words', inplace=True, axis=1)
    return score_series


def normalize(data):
    x = data.values
    min_max_scaler = preprocessing.MinMaxScaler()
    data = pd.DataFrame(min_max_scaler.fit_transform(
        x), index=data.index, columns=data.columns)
    return data


def allto(data):
    data['cumulative'] = ((1/3)*data['cosine_sim'])+((1/3)
                                                     * data['acc_to_post'])+((1/3)*data['acc_to_videos'])
    return data


def home(request):
    return render(request, 'index.html')


def reduceCountry(countryName):
    final = pd.read_csv(
        'C:\\Users\\shash\\Desktop\\Data_Science\\Major2020\\webScrapping/final_dataset.csv', encoding='unicode_escape')
    links = pd.read_excel(
        'C:\\Users\\shash\\Desktop\\Data_Science\\Major2020\\webScrapping/Influencer_with_links.xlsx')
    # links=pd.read_excel('Influencer_with_links.xlsx')
    result = pd.merge(final, links, on="name")
    indexes = result[result['country'].str.lower() !=
                     countryName.lower()].index
    result.drop(indexes, inplace=True)
    result = result.sort_values(by="average_post_likes", ascending=False)
    onCountryFilter = []
    for d in result.values:
        onCountryFilter.append(
            {'name': d[0], 'category': d[10], 'id': d[11], 'src': d[12]})
        if(len(onCountryFilter) == 5):
            return onCountryFilter
    return onCountryFilter


def reducePostLikes(countryName):
    final = pd.read_csv(
        'C:\\Users\\shash\\Desktop\\Data_Science\\Major2020\\webScrapping/final_dataset.csv', encoding='unicode_escape')
    links = pd.read_excel(
        'C:\\Users\\shash\\Desktop\\Data_Science\\Major2020\\webScrapping/Influencer_with_links.xlsx')
    # links=pd.read_excel('Influencer_with_links.xlsx')
    result = pd.merge(final, links, on="name")
    indexes = result[result['country'].str.lower() !=
                     countryName.lower()].index
    result.drop(indexes, inplace=True)
    result = result.sort_values(by="average_post_comments", ascending=False)
    onCountryFilter = []
    for d in result.values:
        onCountryFilter.append(
            {'name': d[0], 'category': d[10], 'id': d[11], 'src': d[12]})
        if(len(onCountryFilter) == 5):
            return onCountryFilter
    return onCountryFilter


def reduceVideoComment(countryName):
    final = pd.read_csv(
        'C:\\Users\\shash\\Desktop\\Data_Science\\Major2020\\webScrapping/final_dataset.csv', encoding='unicode_escape')
    links = pd.read_excel(
        'C:\\Users\\shash\\Desktop\\Data_Science\\Major2020\\webScrapping/Influencer_with_links.xlsx')
    # links=pd.read_excel('Influencer_with_links.xlsx')
    result = pd.merge(final, links, on="name")
    indexes = result[result['country'].str.lower() !=
                     countryName.lower()].index
    result.drop(indexes, inplace=True)
    result = result.sort_values(by="average_videos_comments", ascending=False)
    onCountryFilter = []
    for d in result.values:
        onCountryFilter.append(
            {'name': d[0], 'category': d[10], 'id': d[11], 'src': d[12]})
        if(len(onCountryFilter) == 5):
            return onCountryFilter
    return onCountryFilter


def reduceVideoViews(countryName):
    final = pd.read_csv(
        'C:\\Users\\shash\\Desktop\\Data_Science\\Major2020\\webScrapping/final_dataset.csv', encoding='unicode_escape')
    links = pd.read_excel(
        'C:\\Users\\shash\\Desktop\\Data_Science\\Major2020\\webScrapping/Influencer_with_links.xlsx')
    # links=pd.read_excel('Influencer_with_links.xlsx')
    result = pd.merge(final, links, on="name")
    indexes = result[result['country'].str.lower() !=
                     countryName.lower()].index
    result.drop(indexes, inplace=True)
    result = result.sort_values(by="average_videos_views", ascending=False)
    onCountryFilter = []
    for d in result.values:
        onCountryFilter.append(
            {'name': d[0], 'category': d[10], 'id': d[11], 'src': d[12]})
        if(len(onCountryFilter) == 5):
            return onCountryFilter
    return onCountryFilter


def countryInfluencer(request, countryName):
    onCountryFilter = reduceCountry(countryName)
    onCountryPostLike = reducePostLikes(countryName)
    onCountryVideocomments = reduceVideoComment(countryName)
    onCountryVideoViews = reduceVideoViews(countryName)
    print(onCountryVideocomments)
    return render(request, 'country.html', {'country': countryName, 'onCountryFilter': onCountryFilter, 'onCountryPostLike': onCountryPostLike, 'onCountryVideocomments': onCountryVideocomments, 'onCountryVideoViews': onCountryVideoViews})


def predict(request):
    if request.method == 'GET':
        return render(request, 'predict2.html')
    else:
        onBasisPost.clear()
        onBasisVideos.clear()
        onBasisCosine.clear()
        onBasisAll.clear()

        onBasisPostLinks.clear()
        onBasisVideosLinks.clear()
        onBasisCosineLinks.clear()
        onBasisAllLinks.clear()

        country = request.POST['countries']
        category = request.POST['categories']
        productDescription = request.POST['productDetail']
        hashtags = request.POST['hastags']
        print(country)
        print(category)
        print(productDescription)
        print(hashtags)
        data = redu(category, country)
        print(data)
        cos_data = pd.Series
        cos_data = cosineSimilairty(
            category, country, productDescription, hashtags)
        cos_data = cos_data.iloc[1:]
        cos_data = cos_data.reset_index(drop=True)
        data = data.reset_index(drop=True)
        data["cosine_sim"] = cos_data
        data.drop('description', inplace=True, axis=1)
        data.drop('tagged_names', inplace=True, axis=1)
        data.drop('country', inplace=True, axis=1)
        data.drop('category', inplace=True, axis=1)
        data = data.fillna(0)
        indices = pd.Series(data.name)
        data.drop('name', inplace=True, axis=1)
        data = normalize(data)
        data.insert(0, 'name', indices)
        # data=allto(data)
        # print(data)

        new_data = data.sort_values(by='cosine_sim', ascending=False)
        link_data = pd.read_excel(
            'C:\\Users\\shash\\Desktop\\Data_Science\\Major2020\\webScrapping\\Influencer_with_links.xlsx')
        for d in new_data.values:
            if d[7] != 0:
                onBasisCosine.append({'name': d[0], 'value': d[7]})
                try:
                    val = link_data.set_index('name').to_dict()
                    dd = val['id'][d[0]]
                    print(d[0])
                    onBasisCosineLinks.append({'name': d[0], 'id': (dd)})
                except:
                    print('shashwat')

        data['acc_to_post'] = 0.65*data['average_post_comments'] + \
            0.35*data['average_post_likes']
        new_data = data.sort_values(by='acc_to_post', ascending=False)
        for d in new_data.values:
            if d[8] != 0:
                onBasisPost.append({'name': d[0], 'value': d[8]})
                try:
                    val = link_data.set_index('name').to_dict()
                    dd = val['id'][d[0]]
                    onBasisPostLinks.append({'name': d[0], 'id': (dd)})
                except:
                    pass

        data['acc_to_videos'] = 0.65*data['average_videos_comments'] + \
            0.35*data['average_videos_views']
        new_data = data.sort_values(by='acc_to_videos', ascending=False)
        for d in new_data.values:
            if d[9] != 0:
                onBasisVideos.append({'name': d[0], 'value': d[9]})
                try:
                    val = link_data.set_index('name').to_dict()
                    dd = val['id'][d[0]]
                    onBasisVideosLinks.append({'name': d[0], 'id': (dd)})
                except:
                    pass

        new_data = allto(data)
        new_data = new_data.sort_values(by='cumulative', ascending=False)
        for d in new_data.values:
            if d[10] != 0:
                onBasisAll.append({'name': d[0], 'value': d[11-1]})
                try:
                    val = link_data.set_index('name').to_dict()
                    dd = val['id'][d[0]]
                    onBasisAllLinks.append({'name': d[0], 'id': (dd)})
                except:
                    pass
        return render(request, 'output.html', {'onBasisAllLinks': onBasisAllLinks[0:6], 'onBasisCosineLinks': onBasisCosineLinks[0:6], 'onBasisPostLinks': onBasisPostLinks[0:6], 'onBasisVideosLinks': onBasisVideosLinks[0:6]})


def final_output(request):
    data = {
        "post": onBasisPost[0:6],
        "video": onBasisVideos[0:6],
        "cosine": onBasisCosine[0:6],
        "allto": onBasisAll[0:6]
    }
    return JsonResponse(data)
