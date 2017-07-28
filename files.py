{
  'extnames': [
    'h', 'c', 'cc', 'cpp', 'java'
  ],

  'excludedpatterns': [
    '*test*',
  ],

  'rules': {
    '+': [
      'storage', 'url',
    ],
    'android_webview': {
      '-': [
        'glue',
      ],
    },
  },
}
