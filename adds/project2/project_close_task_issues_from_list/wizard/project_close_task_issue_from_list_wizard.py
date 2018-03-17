from openerp.osv import osv

class project_close_task_issue(osv.osv_memory):
    _name = "project.close.task.issue"
    _description = "Project Close Task and Issues Batch"

    def batch_close_tasks(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        active_ids = context.get('active_ids', []) or []
        task_ids = self.pool['project.task'].browse(cr, uid, active_ids, context=context)
        for task in task_ids:
            close_stage = None
            for stage in task.project_id.type_ids:
                if stage.name == "Closed":
                    task.write({'stage_id': stage.id})
                    break
                if stage.closed and stage.name != "Cancelled":
                    task.write({'stage_id': stage.id})
                    break
        return {'type': 'ir.actions.act_window_close'}

    def batch_close_issues(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        active_ids = context.get('active_ids', []) or []
        issue_ids = self.pool['project.issue'].browse(cr, uid, active_ids, context=context)
        for issue in issue_ids:
            close_stage = None
            for stage in issue.project_id.type_ids:
                if stage.name == "Closed":
                    issue.write({'stage_id': stage.id})
                    break
                if stage.closed and stage.name != "Cancelled":
                    issue.write({'stage_id': stage.id})
                    break                
        return {'type': 'ir.actions.act_window_close'}