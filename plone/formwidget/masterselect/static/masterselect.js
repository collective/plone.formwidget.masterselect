(function($) {
    var cache = {}; // Cache AJAX results
    var masterVocabularyQueue = {};
    var masterVocabularyComplete = {};

    function sprintf(format, etc) {
        var arg = arguments;
        var i = 1;
        return format.replace(/%((%)|s)/g, function (m) { return m[2] || arg[i++] })
    }

    function populateSelectOptions(items) {
        var options = '';
        var selected = '';
          for (var i = 0; i < items.length; i++) {
            selected = items[i].selected ? ' selected="selected"' : '';
            options += sprintf('<option id="%s" value="%s"%s>%s</option>',
                items[i].id, items[i].value, selected, items[i].content);
        }
        return options
    }
    // AJAX vocabulary handling
    function updateSelect(slaveID, data) {
        $(slaveID).closest('select')
            .empty().html( // Replace all options with new ones
                populateSelectOptions(data.items)).end()
            .change()
            .attr('disabled', false);
    };
    function handleMasterVocabularyChange(event) {
        var value = $(this).attr('type') == 'checkbox' ?
            '' + this.checked : $(this).val();
        var slaveID = event.data.slaveID;
        var name = event.data.name;
        var masterID = event.data.masterID;
        var cachekey = [this.id, slaveID, value].join(':');

        // Remove options starting at empty_length (so users won't see old
        // values and disable field
        $(slaveID).find('option').slice(event.data.empty_length).remove();
        $(slaveID).change();
        $(slaveID).closest(':input').attr('disabled', true);

        // NEW:
        // Need to kill child requests as well
        // Its here to be after the 'change' trigger
        if (masterVocabularyQueue[event.data.slaveID]) {
            masterVocabularyQueue[event.data.slaveID].abort();
            delete(masterVocabularyQueue[event.data.slaveID]);
        }

        // Don't initate ajax request if we match a selected field value
        // to a value in prevent_ajax_vlaues
        var prevent_ajax_values = event.data.prevent_ajax_values != undefined ? event.data.prevent_ajax_values : []
        if (typeof prevent_ajax_values == 'string')
            prevent_ajax_values = [prevent_ajax_values];
        // if length of values is 0; allow any value to match (wildcard)
        var val = $(this).attr('type') == 'checkbox' ? this.checked : $(this).val();
        val = prevent_ajax_values.length == 0 ? false : $.inArray(val, prevent_ajax_values) > -1;
        if (val)
            return;

        // Abort and remove any active requests, since only want the latest
        //var queuekey = this.id;
        var queuekey = event.data.masterID;
        if (masterVocabularyQueue[queuekey]) {
            masterVocabularyQueue[queuekey].abort();
            delete(masterVocabularyQueue[queuekey]);
        }
        if (value != null) {
            if (cache[cachekey] == undefined) {

                masterVocabularyQueue[queuekey] = $.getJSON(event.data.url,
                    { field: this.id, name: name, slaveID: slaveID, masterID: masterID, value: value },
                    function(data) {
                        cache[cachekey] = data;
                        updateSelect(slaveID, data);
                    });
                }
            else
                updateSelect(slaveID, cache[cachekey]);
        }
    };
    $.fn.bindMasterSlaveVocabulary = function(data) {
        var trigger = data.initial_trigger ? data.initial_trigger : false;
        // NEW:
        // Disable slave select if empty
        // Only if it's a select field??
        var emptyLength = data.empty_length ? data.empty_length : 0
        var slaveLength = $(data.slaveID)[0].length;
        if (slaveLength <= emptyLength)
            $(data.slaveID).attr('disabled', true);

        $(this).on('change', data, handleMasterVocabularyChange);
        if (trigger)
            $(this).trigger('change');
    };

    // AJAX value handling
    function updateAttr(slaveID, data) {
        $(slaveID).attr(data.attr, data.value).change();
    }
    function handleMasterAttrChange(event) {
        var value = $(this).attr('type') == 'checkbox' ?
            '' + this.checked : $(this).val();
        var slaveID = event.data.slaveID;
        var name = event.data.name;
        var masterID = event.data.masterID;
        var cachekey = [this.id, slaveID, value].join(':');
        if (cache[cachekey] == undefined)
            $.getJSON(event.data.url,
                { field: this.id, slaveID: slaveID, name: name, masterID: masterID, value: value },
                function(data) {
                    cache[cachekey] = data;
                    updateAttr(slaveID, data);
                });
            else updateAttr(slaveID, cache[cachekey]);
    };
    $.fn.bindMasterSlaveAttr = function(data) {
        var trigger = data.initial_trigger ? data.initial_trigger : true;

        $(this).on('change', data, handleMasterAttrChange);
        if (trigger)
            $(this).trigger('change');
    };

    // AJAX value handling
    function updateValue(slaveID, data) {
        var slaveID = event.data.form.find(event.data.slaveID);
        slaveID.val(data).change();
        if (slaveID.is('.kupu-editor-textarea')) // update kupu editor too
            slaveID.siblings('iframe:first').contents().find('body').html(data);
    }
    function handleMasterValueChange(event) {
        var value = $(this).attr('type') == 'checkbox' ?
            '' + this.checked : $(this).val();
        var slaveID = event.data.slaveID;
        var name = event.data.name;
        var masterID = event.data.masterID;
        var cachekey = [this.id, slaveID, value].join(':');
        if (cache[cachekey] == undefined)
            $.getJSON(event.data.url,
                { field: this.id, slaveID: slaveID, name: name, masterID: masterID, value: value },
                function(data) {
                    cache[cachekey] = data;
                    updateValue(slaveID, data);
                });
            else updateValue(slaveID, cache[cachekey]);
    };
    $.fn.bindMasterSlaveValue = function(data) {
        var trigger = data.initial_trigger ? data.initial_trigger : true;
        data.form = $(this).parents('form').first();
        $(this).on('change', data, handleMasterValueChange);
        if (trigger)
            $(this).trigger('change');
    };

    // Field status/visibility toggles
    function handleMasterToggle(event) {
        var action = event.data.action;
        var slaveID = event.data.form.find(event.data.slaveID);

        // toggle not really a toggle; only executes the action when
        // the selected item is choosen, or every time if ()
        var val = $(this).attr('type') == 'checkbox' ? this.checked : $(this).val();

        // if length of values is 0; allow any value to match (wildcard)
        val = event.data.values.length == 0 ? true : $.inArray(val, event.data.values) > -1;

        if ($.inArray(action, ['hide', 'disable']) > -1) {
            val = !val;
            action = action == 'hide' ? 'show' : 'enable';
        }
        // show toggle
        if (action == 'show') {
            var selector = event.data.siblings ? slaveID.parent() : slaveID;
            var css_action =  val ? "show" : "hide";
            var css_option = event.data.initial_trigger ? null : 'fast';
            selector.each(function() { $(this)[css_action](css_option); });
        //enable toggle
        } else
            slaveID.closest(':input').attr('disabled', val ? false : true);
    }
    $.fn.bindMasterSlaveToggle = function(data) {
        var master = $(this);
        data.form = master.parents('form').first();
        var trigger = data.initial_trigger ? data.initial_trigger : true;
        data.initial_trigger = trigger;
        master.on('change', data, handleMasterToggle);
        if (data.initial_trigger) {
            var fieldset_id  = master.closest('fieldset').attr('id');
            if (fieldset_id === undefined || $(fieldset_id).is(":visible")) {
                master.change();
            } else {
                fieldset_id = '#' + fieldset_id;
                var props = { position: 'absolute', visibility: 'hidden', display: 'block' };
                // backup old properties
                var old_props = {};
                for (var name in props) {
                    old_props[name] = $(fieldset_id).css(name);
                }
                // change display and execute change on master
                $(fieldset_id).css(props);
                master.change();
                // set back old properties
                $(fieldset_id).css(old_props);
            }
            data.initial_trigger = false;
        }
    };

})(jQuery);
