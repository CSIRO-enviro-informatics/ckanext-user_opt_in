// Enable JavaScript's strict mode. Strict mode catches some common
// programming errors and throws exceptions, prevents some unsafe actions from
// being taken, and disables some confusing and bad JavaScript features.
"use strict";

ckan.module('user_opt_in_popup', function ($) {
  return {
    initialize: function () {
      var $el = $(this.el);
      var popup = $el.modal({backdrop: 'static'});
      var self = this;
      $el.on('click.user_opt_in.opt_in', '.user_opt_in_set_opt_in', function () {
        self.sandbox.client.call('POST', 'user_opt_in/set', {opted_in: true}, function (res) {
          popup.hide();
        }, function(err) {
          console.error(err);
          popup.hide();
        });
      });
      $el.on('click.user_opt_in.opt_out', '.user_opt_in_set_opt_out', function () {
        self.sandbox.client.call('POST', 'user_opt_in/set', {opted_in: false}, function (res) {
          popup.hide();
        }, function(err) {
          console.error(err);
          popup.hide();
        });
      });

      popup.show();
    }
  };
});
