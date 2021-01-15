import request from '@/utils/request'

export function imgTest() {
  return request({
    url: '/img_test',
    method: 'get'
  })
}

export function test_connection() {
  return request({
    url: '/',
    method: 'get'
  })
}

export function post_style(data) {
  return request({
    url: '/post_style',
    method: 'post',
    data
  })
}

export function img_plus(data) {
  return request({
    url: '/img_plus',
    method: 'post',
    data
  })
}

export function img_waifu(data, param) {
  return request({
    url: '/img_waifu/' + param,
    method: 'post',
    data
  })
}

export function img_transtyle(data, param) {
  return request({
    url: '/img_transtyle/' + param,
    method: 'post',
    data
  })
}

export function img_colorful(data) {
  return request({
    url: '/img_colorful',
    method: 'post',
    data
  })
}

export function img_definition(data) {
  return request({
    url: '/img_definition',
    method: 'post',
    data
  })
}

export function txt_recognize(data, param) {
  return request({
    url: '/txt_recognize/' + param,
    method: 'post',
    data
  })
}
